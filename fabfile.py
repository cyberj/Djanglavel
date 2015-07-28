"""
Fabric Helper to ease Django dev.
http://www.fabfile.org/
"""
import random;
from datetime import datetime
from fabric.api import *
from fabric.utils import puts
from fabric.colors import green, cyan, yellow
from manage import PROJECT_NAME
env.hosts = ['michka.bearstech.com',]
env.user = PROJECT_NAME
env.forward_agent = True

env.project = {}
env.project["name"] = PROJECT_NAME
env.project["db"] = "sqlite"
env.project["git"] = "forge@git.arcagenis.org:%s.git"
env.project["git_branch"] = "dev"
env.project["dev"] = "arcagenis.org"

@task
def localhost():
    """Use localhost context (default)
    """
    env.run, env.cd = local, lcd
    env.hosts = ["localhost"]
    env.project["db"] = "sqlite"
    env.project["path"] = "."
    env.project["vtenvpath"] = env.project["path"]
    env.project["requirements"] = "requirements.txt"
    if env.local_user == "vagrant":
	puts(cyan("Vagrant detected"))
        env.project["vtenvpath"] = "/home/vagrant"
        env.project["requirements"] = "/vagrant/%(name)s/requirements.txt" % env.project
    env.project["backup"] = "./sql"
    env.project["logs"] = "./log"
    env.project["static"] = "./static"
    cmd = ". %(vtenvpath)s/vtenv/bin/activate && %(path)s/manage.py" % env.project
    env.manage = lambda x:local(" ".join((cmd, x)))

# default
localhost()

@task
def pgsql():
    """Set env to pgsql
    """
    env.project["db"] = "pgsql"

@task
def mysql():
    """Set env to mysql
    """
    env.project["db"] = "mysql"

@task
def sqlite():
    """Set env to sqlite
    """
    env.project["db"] = "sqlite"

def dev():
    """Use distant server context
    """
    env.run, env.cd = run, cd
    env.hosts = env.project["dev"]
    env.project["db"] = "mysql"
    env.project["path"] = "root"
    env.project["vtenvpath"] = env.project["path"]
    env.project["backup"] = "sql"
    env.project["requirements"] = "requirements.txt"
    cmd = ". %(vtenvpath)s/vtenv/bin/activate && %(path)s/manage.py" % env.project
    env.manage = lambda x:run(" ".join((cmd, x)))

@task
def syncdb():
    """Create database or syncdb
    """
    puts(green("Doing syncdb"))
    env.run("mkdir -p %s" % env.project["logs"])
    env.manage('syncdb')

@task
def migrate():
    """Migrate database
    """
    puts(green("Doing migrate"))
    env.manage('migrate')

@task
def local_settings(create=False, db=None):
    """Add local_settings.py
    """
    salt = "abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_=+)"
    key = "".join([random.choice(salt) for i in range(50)])
    settings_file = "%(path)s/%(name)s/local_settings.py" % env.project
    db = db or env.project["db"]
    with settings(warn_only=True):
        with hide('warnings'):
            if env.run("test -f %s" % settings_file).failed or create:
                puts("File local_settings.py not found : I create it")
                env.run("rm -f %s" % settings_file)
                env.run('echo "SECRET_KEY = \'%s\'" > %s' % (key, settings_file))

                if db == "mysql":
                    config = (
                        "DATABASES[\'default\'] = {",
                        "    \'ENGINE\': \'django.db.backends.mysql\',",
                        "    \'NAME\': \'%s\'," % env.project["name"],
                        "\'OPTIONS\': {\'read_default_file\':" +
                            " os.path.expanduser(\'~/.my.cnf\'),},",
                        "}"
                    )
                elif db == "sqlite":
                    config = (
                        "DATABASES[\'default\'] = {",
                        "    \'ENGINE\': \'django.db.backends.sqlite3\',",
                        "    \'NAME\': \'db.dat\',",
                        "}"
                    )
                elif db == "pgsql":
                    config = (
                        "DATABASES[\'default\'] = {",
                        "    \'ENGINE\': \'django.db.backends.postgresql_psycopg2\',",
                        "    \'NAME\': \'%s\'," % env.project["name"],
                        "}"
                    )
                config = "\n".join(config)
                env.run('echo "DATABASES = {}\n" >> %s' % (settings_file))
                env.run('echo "%s\n" >> %s' % (config, settings_file))


@task
def test():
    """Test application
    """
    puts(green("Doing tests"))
    env.manage('test')

@task
def collectstatic():
    """Command collect static
    """
    puts(green("Doing collectstatic"))
    env.manage('collectstatic --noinput')

@task
def update():
    """Update env : syncdb, migrate, collectstatic, test
    """
    syncdb()
    migrate()
    collectstatic()
    test()

@task
def prepare():
    """Prepare django env for first install
    """
    local_settings()
    update()

@task
def install():
    """[DISTANT] Remote install
    """
    if "localhost" in env.hosts:
        return
    from fabric.contrib.files import exists
    from fabric.contrib.console import confirm
    if exists(env.project["path"]):
        if not confirm("Project already installed : dump it?", default=False):
            return
        else:
            run("rm -rf %(path)s ." % env.project)

    run("git clone %(git)s %(path)" % env.project)
    with cd(project["path"]):
        if env.project["git_branch"] != "master":
            run("git branch %(git_branch)s origin/%(git_branch)s" % env.project)
        run("git pull -u origin")

@task
def backup(mandatory=True):
    """Backup db
    """
    puts(green("Saving old DB"))
    env.run("mkdir -p %s" % env.project["backup"])
    now = datetime.now()
    bckp_file = now.strftime(env.project["name"]+"-%y-%m-%d_%Hh%Mm%Ss")
    bckp_file = "%(backup)s/" % env.project + bckp_file
    with settings(warn_only=True):
        with hide("warnings"):
            settings_file = "%(path)s/%(name)s/local_settings.py" % env.project
            if env.run("test -f %s" % settings_file).failed:
                puts("Can't find DB")
                if mandatory:
                    abort("Can't find local_settings")
                else:
                    return

            # find actual base
            if env.run("grep mysql %s" % settings_file).succeeded:
                bckp_file += ".sql.gz"
                with settings(warn_only=False):
                    env.run("mysqldump %s | gzip > %s" %
                            (env.project["name"], bckp_file))
            elif env.run("grep sqlite %s" % settings_file).succeeded:
                bckp_file += ".db.dat"
                if env.run("test -f %s/db.dat" % env.project["path"]).failed:
                    with settings(warn_only=False):
                        env.run("sqlite3 %s/db.dat \'\'" % env.project["path"])
                with settings(warn_only=False):
                    env.run("cp %s/db.dat %s" %
                            (env.project["path"], bckp_file))
            elif env.run("grep postgresql %s" % settings_file).succeeded:
                bckp_file += ".sql.gz"
                with settings(warn_only=False):
                    env.run("pg_dump %s | gzip > %s" %
                            (env.project["name"], bckp_file))
            else:
                abort("Can't save db")

            puts(green("Saved to file : " + cyan("%s" % bckp_file)))

@task
def vtenv():
    """Update the vtenv thing
    """
    with env.cd(env.project["vtenvpath"]):
        with settings(warn_only=True):
            with hide("warnings"):
                if env.run("test -d vtenv").failed:
                    with settings(warn_only=False):
                        with show("warnings"):
                            env.run("virtualenv vtenv")
            if env.run("test -e vtenv/bin/pip-2.7").failed:
                env.run("vtenv/bin/pip install -Mr %(requirements)s" % env.project)
            else:
                env.run("vtenv/bin/pip-2.7 install -Mr %(requirements)s" % env.project)

@task
def git_update(mandatory=True):
    """Update git env
    """
    with env.cd(env.project["path"]):
        puts(green("Updating code..."))
        with hide('running', 'stdout', 'stderr'):
            commit = env.run("echo `git show -s --format=\"%h\"`")
            subject = env.run("echo `git show -s --format=\"%s\"`")
        env.run("git pull")
        puts(green("Previous git HEAD was : ") +
              cyan(commit.strip()) + " " +
              yellow(subject.strip()))
        with hide('running', 'stdout', 'stderr'):
            commit = env.run("echo `git show -s --format=\"%h\"`")
            subject = env.run("echo `git show -s --format=\"%s\"`")
        puts(green("Code updated to : ") +
              cyan(commit.strip()) + " " +
              yellow(subject.strip()))
        puts(green("Updating vtenv"))
        env.run("./vtenv.sh")

@task
def mrproper():
    """Clean env
    """
    with env.cd(env.project["path"]):
        env.run("git clean -fdx")
        env.run("rm -rf vtenv")

@task
def pyc():
    """Remove *.pyc
    """
    with env.cd(env.project["path"]):
        env.run("find . -iname \"*.pyc\" -delete")

@task
def deploy():
    """Update django env
    """
    if not "localhost" in env.hosts:
        install()
    local_settings()
    backup()
    vtenv()
    if not "localhost" in env.hosts:
        git_update()
    syncdb()
    migrate()
    collectstatic()
    test()
    puts(green("Reload app"))
    with env.cd(env.project["path"]):
        env.run("touch %(name)s/wsgi.py" % env.project)
    #with cd("root/docs"):
    #    print(green("Updating documentation"))
    #    run("../vtenv/bin/sphinx-build -b html -d _build/doctrees . _build/html")
    puts(green("Application deployed"))


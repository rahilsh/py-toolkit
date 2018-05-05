import datetime
import glob
import os
import re
import time


def process_app_folder(app, builds, delete_older_than_days):
    builds.sort(key=lambda x: os.path.getmtime(x), reverse=False)
    builds.pop()
    builds = filter(
        lambda x: (
                (time.time() - os.path.getmtime(x)) // (
                24 * 3600) >= delete_older_than_days),
        builds)

    for build in builds:
        print re.match(r'[0-9.]+.*', os.path.basename(build))
        print "Deleting {} of {} since it is Older than 7 days".format(os.path.basename(build), os.path.basename(app))
        # shutil.rmtree(build)


def print_build_creation_time(builds):
    for build in builds:
        print "Build: {}. Created on: {}".format(os.path.basename(build),
                                                 datetime.datetime.fromtimestamp(os.path.getmtime(build)).strftime(
                                                     '%Y-%m-%d %H:%M:%S.%f'))


def main():
    print "Running at {}".format(datetime.datetime.fromtimestamp(time.time()).strftime(
        '%Y-%m-%d %H:%M:%S.%f'))
    path_to_clean = '/Users/rahil.r/Documents/oms/'
    delete_older_than_days = 2
    apps = filter(os.path.isdir, glob.glob(path_to_clean + "*"))
    apps.sort(key=lambda x: os.path.getmtime(x))

    for app in apps:
        print "=====Processing : {}=====".format(os.path.basename(app))
        all_builds = filter(os.path.isdir, glob.glob(app + '/' "*"))
        all_builds.sort(key=lambda x: os.path.getmtime(x), reverse=False)

        snapshot_builds = filter(lambda x: x.endswith(
            '-SNAPSHOT'), all_builds)
        print_build_creation_time(snapshot_builds)
        if len(snapshot_builds) > 0:
            process_app_folder(app, snapshot_builds, delete_older_than_days)
        else:
            print "No SNAPSHOT build"
        print
        # release_builds = filter(lambda x: not x.endswith(
        #     '-SNAPSHOT'), all_builds)
        # print_build_creation_time(release_builds)
        # process_app_folder(app, release_builds, delete_older_than_days)
        # print


if __name__ == '__main__':
    main()

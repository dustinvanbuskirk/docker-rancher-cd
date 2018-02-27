import sys
import getopt
import os
import subprocess
import yaml


def main(argv):
    def set_image(service, image, working_directory):
        print(service)
        print(image)
        print(os.listdir(working_directory))
        with open(working_directory + 'docker-compose.yml') as f:
            doc = yaml.load(f)

        doc['services'][service]['image'] = image
        with open(working_directory + 'docker-compose.yml', 'w') as f:
            yaml.dump(doc, f)

    rancher_compose_options = ''
    rancher_compose_command = ''
    rancher_compose_args = ''
    rancher_catalog_template_directory = '/codefresh/volume/rancher-catalog/templates'
    rancher_catalog_template_name = None
    rancher_catalog_template_version = None

    try:
        opts, args = getopt.getopt(argv, "o:c:a:t:n:v:i:s:",
                                   ["help", "rancher_compose_options=", "rancher_compose_command=", "rancher_compose_args=", "rancher_catalog_template_directory=",
                                    "rancher_catalog_template_name=", "rancher_catalog_template_version", "image", "service"])
    except getopt.GetoptError:
        print('Unrecognized Argument, See Usage Below.')
        print('rancher-compose.py -n "<CATALOG_TEMPLATE_NAME>" -o "<OPTIONS>" -c "<COMMAND>" -a "<args>"')
        print('to see rancher-compose help for a run rancher-compose.py help with no additional command line args')
        print('to see rancher-compose help for a COMMAND run rancher-compose.py -c "<COMMAND>" -a "--help" with no additional command line args')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "--help":
            print('rancher-compose.py -n <rancher_catalog_template_name> -o <rancher_compose_options> -c <rancher_command> -a <rancher_args>')
            print('rancher_catalog_template_directory - templates directory for catalog')
            print('rancher_catalog_template_name - template name for catalog')
            print('rancher_catalog_template_version - template version for catalog if this is not set defaults to latest')
            print('rancher_compose_options - arguments to pass to rancher, --debug --version')
            print('rancher_compose_command - arguments to pass to rancher, inspect')
            print('rancher_compose_args - COMMAND arguments to pass to rancher')
            command = ['rancher-compose --help']
            proc = subprocess.Popen(command, shell=True)
            stdout, stderr = proc.communicate()
            sys.exit()
        elif opt in ("-o", "--rancher_compose_options"):
            rancher_compose_options = arg
        elif opt in ("-c", "--rancher_compose_command"):
            rancher_compose_command = arg
        elif opt in ("-a", "--rancher_compose_args"):
            rancher_compose_args = arg
        elif opt in ("-t", "--rancher_catalog_template_directory"):
            rancher_catalog_template_directory = arg
        elif opt in ("-n", "--rancher_catalog_template_name"):
            rancher_catalog_template_name = arg
        elif opt in ("-v", "--rancher_catalog_template_version"):
            rancher_catalog_template_version = arg
        elif opt in ("-s", "--service"):
            service = arg
        elif opt in ("-i", "--image"):
            image = arg

    template_directory = rancher_catalog_template_directory + '/' + rancher_catalog_template_name

    # If no version given select latest version

    if rancher_catalog_template_version is None:
        sorted_directories = sorted([int(x) for x in os.listdir(template_directory) if x.isdigit()], reverse=True)
        rancher_catalog_template_version = sorted_directories[0]

    working_directory = template_directory + '/' + str(rancher_catalog_template_version) + '/'

    print('Using Catalog Entry: ' + working_directory)

    set_image(service, image, working_directory)

    command = ['rancher-compose ' + rancher_compose_options + ' ' + rancher_compose_command + ' ' + rancher_compose_args]
    exitcode = subprocess.Popen(command, shell=True, cwd=working_directory, stdout=sys.stdout, stderr=sys.stderr).wait()

    exit(exitcode)


if __name__ == "__main__":
    main(sys.argv[1:])

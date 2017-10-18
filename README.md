# docker-rancher-cd

## Script Library

### rancher-compose.py

Allows you to use Rancher Compose https://github.com/rancher/rancher-compose for CD

Example run from rancher-catalog local directory.

```console
docker run -v `pwd`:/rancher-catalog sctechdev/hawthorne-utils:test rancher-compose.py -o options -a  args -t /rancher-catalog/templates/ -n presenceweb
```

Codefresh Build Step to execute Rancher Service Upgrade

All `${{var}}` variables must be put into Codefresh Build Parameters

This is designed to work with a private Rancher Catalog.

GITHUB_TOKEN - Token Generated on GitHub

If you wish to pull from another repository you may need to modify the git clone command.

Required Values:

`RANCHER_URL` - Rancher URL `https://rancher.mydomain.com`

`RANCHER_ACCESS_KEY` - Rancher API Access Key for Rancher User or Rancher Environment

`RANCHER_SECRET_KEY` - Rancher API Secret Key that corresponds with the RANCHER_ACCESS_KEY

`RANCHER_CATALOG_TEMPLATE_NAME` - Name of the folder holding the Catalog template for your Stack

`RANCHER_STACK_NAME` - Stack Name to run Upgrade against 

`RANCHER_SERVICE_NAME` - Serivce Name to Upgrade

This currently confirms upgrades automatically and uses Dockr image tag oflatest but later versions will allow for some API or HTTP checked before confirmation and specification of the image tag from your codefresh.yml.

This also automatically selects latest version of your Catalog Template.  If you wish to override this you will need to add `-v <folder number>` to list of parameters passed to script.

codefresh.yml
```console
  buildimage:
    type: build
    title: Build Runtime Image
    dockerfile: Dockerfile
    image_name: # Image you're building/scanning [repository/image]
    tag: latest-cf-build-candidate

  git_clone_rancher_catalog_repo:
    title: Clone Rancher Catalog
    image: codefreshio/git-image:latest
    working_directory: ${{main_clone}}
    commands:
      - bash -c "rm -rf /codefresh/volume/rancher-catalog/"
      - bash -c "git clone https://${{GITHUB_TOKEN}}:x-oauth-basic@github.com/SC-TechDev/rancher-catalog.git /codefresh/volume/rancher-catalog"
    when:
      branch:
        only:
          - master

  upgrade_service:
    title: Upgrade Rancher Service
    image: sctechdev/docker-rancher-cd:latest
    commands:
      - /usr/bin/python3 /scripts/rancher-compose.py -n "${{RANCHER_CATALOG_TEMPLATE_NAME}}" -o "--url ${{RANCHER_URL}} --access-key ${{RANCHER_ACCESS_KEY}} --secret-key ${{RANCHER_SECRET_KEY}} --project-name ${{RANCHER_STACK_NAME}} up" -c "${{RANCHER_SERVICE_NAME}} --upgrade --confirm-upgrade --force-upgrade --pull -d"
    when:
      branch:
        only:
          - master
```

## Rancher CLI Still Work in Progress
### rancher-cli.py

Allows you to use Rancher CLI http://docs.rancher.com/rancher/v1.2/en/cli/

Linux:
```console
$ docker run -it --rm --net host sctechdev/hawthorne-utils:latest rancher-cli.py -o "<OPTIONS>" -c "<COMMAND>" -a "<args>"
```

Pull Requests are Welcome!

Just fork this Repository, Branch and make a Pull Request back!
https://help.github.com/articles/creating-a-pull-request-from-a-fork/

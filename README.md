# `This` Docker Image is use for creating the pjsua2 python module.

#### Using this Docker Image you can able to extract the pjsua2 folder.

##### You Need to Map the Volume in the container Working Directory /app.

##### Follow the Steps to get the pip3 module and libs folder what is use of this folder We Explained Below.

**steps to build and map the volume :**

- Use of below command cloning the image from the external registry from docker.

```bash

docker pull gunaneelamegam/pjsua2

When using the command we can able to get the image locally.
```

- After building the image as locally needs to verify if the image is present (or) not .

```bash

    docker images
```

- After that you ready to use the image as a container.

  - where ever we use {user-defined} needs to replaced by your self.

  - your's preferable name for example.

`Example1 :`

```bash
 docker  run -it --name {user-defined} -v {user-defined}:/{any-where inside container} {image-name} /bin/bash
```

- If you not clear on before example please be copy and paste the command.

`Example :`

```bash

docker run -it --name pjsua2-builder -v $(pwd):/test gunaneelamegam/pjsua2 /bin/bash
```

**NOTE:**

```bash
* After executing the previous command in you terminal you able to move inside the container.

* you mounted inside the /test folder which you mapped when execute the run command.

* cd /app

NOTE:
    * what ever you need from this container you need to move to the mapped directory.

    cd /app
    cp -r ./pjsua2 /test
    cp -r ./pjproject-2.12 /test
    cp -r ./lib /test

* After executing above command inside the container bash or terminal.

* exit the docker container using ctrl-c or exit.

```

- `Finally` which directory you mapped when docker run command with -v option all the copied folders where present inside the host machine.

              Happy Coding ...

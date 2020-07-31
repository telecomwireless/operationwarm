## Installing and Running the application

The easiest way to run this application on your machine is through [docker](https://www.docker.com/) software.

1. Download Docker Desktop software.

    - Windows users use [this](https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe) to download the latest stable version. To install Docker Desktop on windows you need to meet following [system requirements](https://docs.docker.com/docker-for-windows/install/#system-requirements).
    
    - Mac users use [this](https://download.docker.com/mac/stable/Docker.dmg) to download the latest stable version. You need to meet following [system requirements](https://docs.docker.com/docker-for-windows/install/#system-requirements) before to install on mac.

2. Follow below installation instructions to install and start docker.

   - [Windows](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-desktop-on-mac)
   - [Mac](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-desktop-on-mac)
   
3. Once docker is installed, you need to pull the image from docker hub. Just copy paste below
   command on to window's powershell or mac terminal.
   
   `docker pull kcnagareddy/operationwarm`
   
4. Once the image is downloaded, you can use docker run command like shown below to start the application.

   `docker run -p 8050:8050 kcnagareddy/operationwarm`

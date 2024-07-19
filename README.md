## Docker

```
docker build -t my-flask-app .
docker run -p 4000:80 my-flask-app
```

This will map port 80 in the container to port 4000 on your host machine. Modify the port mapping as necessary for your application.


Build it: `docker build -t my-flask-app .`  
Run it: `docker run -p 4000:80 my-flask-app`  
View webapp: `http://localhost:4000/`

To open the web app for the Flask app running in a Docker container, you'll need to know two things:

1. **The IP address of the host machine where Docker is running**: 
   - If you're running Docker on your local machine, the IP address is typically `localhost` or `127.0.0.1`.
   - If Docker is running on an EC2 instance on AWS or another remote server, you'll need the public IP address or DNS name of that server.

2. **The port number that you've exposed and mapped to your Docker container**:
   - In the `docker run` command, you specify port mapping. For example, if you used `-p 4000:80`, `4000` is the host port that is mapped to the `80` port inside the container.

Assuming you're running Docker on your local machine and used the port mapping `-p 4000:80`, you would open your web browser and go to:

```
http://localhost:4000
```

Or:

```
http://127.0.0.1:4000
```

If the Docker container is running on an EC2 instance or a remote server, replace `localhost` with the public IP address or the public DNS name provided by AWS for that EC2 instance, followed by the port number you mapped when you ran the container:

```
http://<EC2_Public_IP_or_Public_DNS>:4000
```

Make sure that the security group associated with your EC2 instance allows inbound traffic on the port you've mapped (in this case, port 4000) to allow you to access the Flask app from your web browser.

## EC2

#### Logging into EC2
```
ssh -i kp.pem ubuntu@**.***.***.***
```

To log out from an EC2 instance after you've finished your SSH session, you can simply type exit or press Ctrl+D. This will end the SSH session and log you out, returning you to your local machine's command prompt or terminal.
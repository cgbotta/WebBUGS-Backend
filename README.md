1. Work on code in this directory
2. Test locally
   - ```docker build -t flask-container .```
   - ```docker run -p 3000:3000 flask-container```
   - ```curl localhost:3000```
3. Push container to Lightsail
   - ```aws lightsail push-container-image --service-name flask-service --label flask-container --image flask-container```
4. Deploy container to Lightsail
   - Change image to correct version in container.json
   - ```aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json```
5. Check deployment status
   - ```aws lightsail get-container-services --service-name flask-service```
6. When RUNNING is shown, it is done!

Instructions from here: https://aws.amazon.com/tutorials/serve-a-flask-app/
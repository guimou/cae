### Model Training
1. Uncompress credicard.csv from data folder
2. Use notebook in train folder to create the model file

### Manual Deployment of model (using Flask)
1. From the manual/container folder

2. Test the code:
python ccfd.py

curl -X POST -H 'Content-Type: application/json' -d '{"strData": "0.365194527642578,0.819750231339882,-0.5927999453145171,-0.619484351930421,-2.84752569239798,1.48432160780265,0.499518887687186,72.98"}' http://127.0.0.1:8080

3. Build docker image
docker build . -t ccfd-modelfull:0.1.1

docker run -it --rm -p 127.0.0.1:8080:8080 ccfd-modelfull:0.1.1

docker tag ccfd-modelfull:0.1.1 quay.io/guimou/ccfd-modelfull:0.1.1  (change destination repo)
docker push quay.io/guimou/ccfd-modelfull:0.1.1

4. Create the application from OpenShift UI
    - Create a project
    - Go to the Developper view
    - Click on "Add" and select "From container image"
    - Use repo address for the container image
    - Check "Create Route"
    - Wait for deployment

5. Test
curl -X POST -H 'Content-Type: application/json' -d '{"strData": "0.365194527642578,0.819750231339882,-0.5927999453145171,-0.619484351930421,-2.84752569239798,1.48432160780265,0.499518887687186,72.98"}' http://ccfd-modelfull-cae2.apps.perf3.chris.ocs.ninja/   (change address with created Route)



### Seldon basic
1. Check and apply deployment from seldon-base folder

2. Create Route to the Service (Seldon does not create the Route exposing the Service to the outside world)

3. Test
curl -s -d '{"data": {"ndarray":[[1.0, 2.0, 5.0, 6.0]]}}'    -X POST http://sklearn-default-classifier-odh.apps.perf3.chris.ocs.ninja/api/v1.0/predictions    -H "Content-Type: application/json"


### Usign Seldon to package CCFD
1. From the seldon/container folder

2. Create modelfull container (change repo and images names)
s2i build . seldonio/seldon-core-s2i-python3:1.2.2 ccfd-modelfull:0.0.1
docker tag ccfd-modelfull:0.0.1 quay.io/guimou/ccfd-modelfull:0.0.1
docker push quay.io/guimou/ccfd-modelfull:0.0.1

5. Create SeldonDeployment as shown in seldon/deploy folder

6. Create Route to the Service (Seldon does not create the Route exposing the Service to the outside world)

7. Test:
curl -X POST -H 'Content-Type: application/json' -d '{"strData": "0.365194527642578,0.819750231339882,-0.5927999453145171,-0.619484351930421,-2.84752569239798,1.48432160780265,0.499518887687186,72.98"}' http://test-odh.apps.perf3.chris.ocs.ninja/api/v1.0/predictions
eval $(minishift docker-env)
VERSION=`date +%s`
docker build -t bmoussaud/setlistfm_service .
docker tag bmoussaud/setlistfm_service:latest bmoussaud/setlistfm_service:${VERSION}
sed s/VERSION/${VERSION}/g deploy/deployit-manifest.template.xml > deploy/deployit-manifest.xml

rm /tmp/test1-1.0.dar
jar cvf /tmp/test1-1.0.dar -C deploy .

XL_DEPLOY_URL=http://localhost:4516
XL_DEPLOY_USERNAME=admin
XL_DEPLOY_PASSWORD=admin

curl -u${XL_DEPLOY_USERNAME}:${XL_DEPLOY_PASSWORD} -X POST -H "content-type:multipart/form-data" ${XL_DEPLOY_URL}/deployit/package/upload/Test.dar -F fileData=@/tmp/test1-1.0.dar


#xld deploy
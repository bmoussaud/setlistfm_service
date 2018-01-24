node {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
        //git 'https://github.com/bmoussaud/SpotifySetList.git'
    }

    stage('Build image') {
        withDockerServer([credentialsId: 'SEDEMO', uri: 'tcp://192.168.99.100:2376']) {
            app = docker.build("bmoussaud/setlistfm_service")
        }
    }

    stage('Package') {
            xldCreatePackage artifactsPath: 'deploy', manifestPath: 'deploy/deployit-manifest.xml', darPath: '$JOB_NAME-0.$BUILD_NUMBER.dar'
            xldPublishPackage serverCredentials: 'Administrateur', darPath: '$JOB_NAME-0.$BUILD_NUMBER.dar'
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        withDockerServer([credentialsId: 'SEDEMO', uri: 'tcp://192.168.99.100:2376']) {
            docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                app.push("0.${env.BUILD_NUMBER}")
                app.push("latest")
            }
        }
    }

    //stage('Deploy to Dev ') {
    //    xldDeploy serverCredentials: 'Administrateur', environmentId: 'Environments/Containers/Kubernetes', packageId: 'Applications/spotify-setlist/0.$BUILD_NUMBER'
    //}


}
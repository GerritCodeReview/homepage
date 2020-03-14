node("jekyll") {
    checkout scm
    stage("generate plugins page") {
        withEnv(['LC_ALL=C.UTF-8', 'LANG=C.UTF-8']) {
            withCredentials([usernamePassword(credentialsId: "gerrit-review.googlesource.com", usernameVariable: "user", passwordVariable: "password")]) {
                sh 'echo $user | wc -c'
                sh 'echo $password | wc -c'
                sh "echo '' > /home/jenkins/.netrc"
                sh "pipenv install --dev"
                sh "pipenv run python tools/plugins.py"
            }
        }
    }
    stage("build homepage") {
        sh "bundle install"
        sh "bundle exec jekyll build"
    }
    stage("deploy homepage") {
        withCredentials([string(credentialsId: "firebase", variable: "FIREBASE_TOKEN")]) {
            sh "firebase use default"
            sh "firebase deploy"
        }
    }
}
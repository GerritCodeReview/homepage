node("jekyll") {
    checkout scm

    def changedFiles = []
    try {
        def previousCommit = env.GIT_PREVIOUS_SUCCESSFUL_COMMIT ?: "HEAD~1"
        changedFiles = sh(
            script: "git diff --name-only ${previousCommit} ${env.GIT_COMMIT}",
            returnStdout: true
        ).trim().split("\n").findAll { it }
    } catch (e) {
        echo "Could not determine changed files (${e.message}), falling back to a full build"
    }
    def summitOnly = changedFiles && changedFiles.every { it.startsWith("summit/2026/") }

    stage("publish summit 2026") {
        dir("summit/2026") {
            sh "bundle install"
            sh "bundle exec jekyll build --config _config.yml,_config_local.yml"
        }
        // TODO: create these three credentials in Jenkins once the SFTP server
        // details are decided:
        //   summit26-sftp       - SSH Username with private key
        //   summit26-sftp-host  - Secret text (hostname or host:port)
        //   summit26-sftp-path  - Secret text (remote destination path)
        withCredentials([
            sshUserPrivateKey(credentialsId: "summit26-sftp", keyFileVariable: "SFTP_KEY", usernameVariable: "SFTP_USER"),
            string(credentialsId: "summit26-sftp-host", variable: "SFTP_HOST"),
            string(credentialsId: "summit26-sftp-path", variable: "SFTP_REMOTE_PATH")
        ]) {
            sh """
                sftp -o StrictHostKeyChecking=no -i \$SFTP_KEY \$SFTP_USER@\$SFTP_HOST <<SFTP_EOF
put -r summit/2026/_site \$SFTP_REMOTE_PATH
SFTP_EOF
            """
        }
    }

    if (!summitOnly) {
        stage("generate plugins page") {
            withEnv(['LC_ALL=C.UTF-8', 'LANG=C.UTF-8']) {
                withCredentials([usernamePassword(credentialsId: "gerrit-review.googlesource.com", usernameVariable: "username", passwordVariable: "password")]) {
                    sh "pipenv install --dev"
                    sh "pipenv run python tools/plugins.py --sleep 30"
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
}

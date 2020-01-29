var urlParams = new URLSearchParams(window.location.search)
var code = urlParams.get("code")
var google_state = urlParams.get("state")

var google_options = {
    client_id: "643017558290-r4ksamj17opnug9gktl3fvmu31pg7b2p.apps.googleusercontent.com",
    client_secret : "kUEQBlNvrUQY8PTG7rug6NlM",
    state : "google",
    response_type: "code",
    scope: "openid email",
    redirect_uri: "http://localhost:5500",
    nonce: "nonce",
    grant_type: "authorization_code"

}

var google_jwt_authorize = () => {
    var authorize_url = `https://accounts.google.com/o/oauth2/v2/auth?response_type=${google_options.response_type}&client_id=${google_options.client_id}&redirect_uri=${google_options.redirect_uri}&state=${google_options.state}&nonce=${google_options.nonce}&scope=${google_options.scope}`
    window.location.href=authorize_url   
}

var google_jwt_token = async () => {

            var token_url = "https://oauth2.googleapis.com/token"
            var data = {
                code: code,
                client_id: google_options.client_id,
                client_secret: google_options.client_secret,
                redirect_uri: google_options.redirect_uri,
                grant_type: google_options.grant_type
            }
            var formBody = Object.keys(data).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key])).join('&')
            var res = await fetch(token_url, {
                method:"POST",
                mode:"cors",
                body: formBody,
                headers:{"Content-Type":"application/x-www-form-urlencoded"}
            })
            var resp = await res.json()
            console.log(resp)
            document.getElementById("id_token").innerText = resp.id_token

}

if(google_state){
    if(code){
        google_jwt_token()
        window.history.replaceState("", "Get Jwt", "http://localhost:5500")
    }
}
function lookUp(method, endpoint, callback, data){
  let JsonData;
  if(data){
    JsonData = JSON.stringify(data)
  }

  const xhr = new XMLHttpRequest()
  const url = `http://localhost:8000/api${endpoint}`
  xhr.responseType= 'json'
  xhr.open(method, url)
  xhr.onload = function(){
      callback(xhr.response, xhr.status)     
  }
  xhr.onerror = function(e){
    callback({'message':'There was an error while making the request!'},400)
  }
  xhr.send(JsonData)
}

export function loadtweets(callback){
    lookUp('GET','/tweets',callback)
  }
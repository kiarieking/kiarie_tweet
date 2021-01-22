import React, {useEffect, useState} from 'react'
import {loadtweets} from '../lookup'
 export function TweetList(props){
    const [tweets, setTweets] = useState([])
    useEffect(()=>{
      const callback = (response, status)=>{
        if (status===200){
        setTweets(response)
        }
        else{
          alert("There was an error!")
        }
      }
      loadtweets(callback)
    },[])
  
    return tweets.map((item, index)=>{
      return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`}/>
    })
  }

export function Actionbtn(props){
    const {tweet, action} = props
    const className = props.className ? props.className : 'btn btn-primary'
    const actionDisplay = action.display ? action.display : 'Action'
    const display = action.type === 'like' ? `${tweet.likes} ${actionDisplay}`: actionDisplay
    return<button className={className} > {display} </button> 
  }
  
  export function Tweet(props){
    const {tweet} = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
     <p>{tweet.id} - {tweet.content}</p>
     <div className='btn btn-group'>
       <Actionbtn tweet={tweet} action={{type:'like', display:'likes'}} className='btn btn-outline-success'/>
       <Actionbtn tweet={tweet} action={{type:'unlike', display:'unlike'}}className='btn btn-outline-secondary'/>
       <Actionbtn tweet={tweet} action={{type:'retweet', display:'retweet'}} className='btn btn-outline-primary'/>
       
     </div>
    </div>
  }
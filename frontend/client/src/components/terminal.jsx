import { useState, useEffect } from 'react'

export default function Terminal(){

    const [userText, setUserText] = useState("")
    const [pastText, setPastText] = useState("")

    let promptStart = "Prompt>> "

    function handleKeyDown(e) {
        if (event.key == 'Enter'){

            let ret = processCommand(userText)
            setPastText( pastText => (ret));
            
            setUserText("")
        }
    }

    function processCommand(command){

        if (command == ""){
            return ""
        }

        let words = command.split(" ");

        // new process - np
        if (words[0] === "np"){
            let p_name = "User Process"

            if (words.length > 1){
                p_name = words[1]
            }

            fetch("http://127.0.0.1:5000/addProcess", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: p_name })
                })
            .catch(console.error);

            return "Process Created"
        }
        // kill process - kill
        else if (words[0] === "kill"){

            if (words.length < 2){
                return "Incorrect usage. Correct: 'kill <processID>'"
            }



            fetch("http://127.0.0.1:5000/killProcess", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: words[1] })
                })
            .catch(console.error);

            return "Process Killed"
        }
        // help - help
        else if (words[0] === "help"){
            return "help -> help   .   .   .   .   np -> new process"
        }
        // unknown command
        else{
            return "Unknown command. Try 'help' to learn more."
        }
    }


    return (
        <div id="terminal">

            {pastText}
            <p>
                {promptStart}
                <input type="text" value={userText} id="userSpace" onChange={e => setUserText(e.target.value)} onKeyDown={handleKeyDown} />
            </p>
            
        </div>
    )

}
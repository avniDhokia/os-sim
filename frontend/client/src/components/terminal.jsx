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

        // new process - np
        if (command.startsWith("np")){
            fetch("http://127.0.0.1:5000/addProcess", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: "test" })
                })
            .catch(console.error);

            return "Process Created"
        }
        // help - help
        else if (command.startsWith("help")){
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
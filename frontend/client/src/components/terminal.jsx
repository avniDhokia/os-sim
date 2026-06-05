import { useState, useEffect } from 'react'
import { sendChangeScheduler, sendKillProcess, sendNewProcess } from '../comms'

// help text with command usage info
function HelpText(){
    return (
        <div>

            {/* help */}
            <p><strong>help</strong></p>
            <p><em>show help menu</em></p>

            <br />

            {/* new process */}
            <p><strong>np [process_name]</strong></p>
            <p><em>create new process</em></p>

            <br />

            {/* kill process */}
            <p><strong>kill process_id</strong></p>
            <p><em>kill specific process</em></p>

            <br />

        </div>
    )
}



export default function Terminal(){

    const [userText, setUserText] = useState("")
    const [pastText, setPastText] = useState("")

    const [showHelp, setShowHelp] = useState(true)

    let promptStart = "Prompt>> "

    function handleKeyDown(e) {
        if (event.key == 'Enter'){

            setShowHelp(false)
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

            sendNewProcess(p_name)
            return "Process Created"
        }
        // kill process - kill
        else if (words[0] === "kill"){

            if (words.length < 2){
                return "Incorrect usage. Try 'help' to learn more"
            }

            sendKillProcess(words[1])
            return "Process Killed"
        }
        // help - help
        else if (words[0] === "help"){
            setShowHelp(true)
        }
        // unknown command
        else{
            return "Unknown command. Try 'help' to learn more."
        }
    }


    return (
        <div id="terminal">

            {showHelp && (
                <HelpText />
            )}
            

            {pastText}
            <p>
                {promptStart}
                <input type="text" value={userText} id="userSpace" onChange={e => setUserText(e.target.value)} onKeyDown={handleKeyDown} />
            </p>
            
        </div>
    )

}
import ProcessComp from "./processComp";


export default function CPU({currentProcess, events}){

    return(
        <div id="cpu" class="component">

            <h1>CPU</h1>

            {events.includes("switch") && (
                <p class="alert">Process Switch</p>
            )}

            {currentProcess && currentProcess.name && (
                <ProcessComp pid={currentProcess.pid} name={currentProcess.name} state={currentProcess.state} priority={currentProcess.priority} timeRan={currentProcess.time_ran} timeToRun={currentProcess.time_to_run} />
            )}
            {(!currentProcess || !currentProcess.name) && (
                <>
                    <p>Idle</p>
                </>
                
            )}

        </div>
    )
}

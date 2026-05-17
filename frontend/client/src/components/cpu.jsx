import ProcessComp from "./processComp";


export default function CPU({currentProcess}){
    console.log(currentProcess)
    return(
        <div id="cpu" class="component">

            <h1>CPU</h1>

            {currentProcess && currentProcess.pid && (
                <ProcessComp pid={currentProcess.pid} name={currentProcess.name} state={currentProcess.state} priority={currentProcess.priority} timeRan={currentProcess.time_ran} timeToRun={currentProcess.time_to_run} />
            )}
            {(!currentProcess || !currentProcess.pid) && (
                <>
                    <p>Idle</p>
                </>
                
            )}

        </div>
    )
}

import ProcessComp from "./processComp";


export default function CPU({currentProcess}){
    console.log(currentProcess)
    return(
        <div id="cpu" class="component">

            <p>CPU</p>

            {currentProcess && (
                <ProcessComp pid={currentProcess.pid} name={currentProcess.name} state={currentProcess.state} priority={currentProcess.priority} timeRan={currentProcess.time_ran} timeToRun={currentProcess.time_to_run} />
            )}
            {!currentProcess && (
                <p>Idle</p>
            )}

        </div>
    )
}

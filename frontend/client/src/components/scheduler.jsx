import ProcessComp from './processComp'

export default function Scheduler({name, currentProcess, state}){
    console.log(state.processes)
    return(
        <div id="scheduler" class="component">

            <h1>{name}</h1>
            
            {/* if there is a currently running process, display it */}
            {state.currentProcess && (
                <ProcessComp pid={currentProcess.pid} name={currentProcess.name} state={currentProcess.state} priority={currentProcess.priority} timeRan={currentProcess.time_ran} timeToRun={currentProcess.time_to_run} />
            )}
            {!state.currentProcess && (
                <p>No currently running process</p>
            )}



            {/* if there are queued processes, display them */}
            {state.processes && (
                <div class="processQueue">
                    {state.processes.map(p => <ProcessComp pid={p.pid} name={p.name} state={p.state} priority={p.priority} timeRan={p.time_ran} timeToRun={p.time_to_run} />)}
                </div>
            )}
            {!state.processes && (
                <p>No Processes</p>
            )}

        </div>
    )
}

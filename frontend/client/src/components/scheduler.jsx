import ProcessComp from './processComp'

export default function Scheduler({name, currentProcess, state}){

    // multi level feedback queue scheduler
    if (name == "Multi-level Feedback Queue Scheduler"){
        <h1>{name}</h1>

        {/* if there are queued processes, display them */}
        {state.processes && (
            <div class="processQueue">
                {state.processes.map(p => <ProcessComp pid={p.pid} name={p.name} state={p.state} priority={p.priority} timeRan={p.time_ran} timeToRun={p.time_to_run} />)}
            </div>
        )}
        {!state.processes && (
            <p>No Processes</p>
        )}
    }

    // FIFO and Round Robin schedulers:
    return(
        <div id="scheduler" class="component">

            <h1>{name}</h1>
            
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

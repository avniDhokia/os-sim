import ProcessComp from './processComp'
import Scheduler from './scheduler';

export default function OperatingSystem({os, cpu, scheduler}){
    console.log(os)
    return (
        <div id="operatingSystem">

            <Scheduler name={scheduler.name} currentProcess={cpu.currentProcess} state={scheduler.state} events={scheduler.events}/>


            {/* if there are queues, display them */}
            <div class="blockedProcessList">
                <h2>Blocked Process List</h2>
                {os.blockedProcesses.processes && os.blockedProcesses.processes.length > 0 ? (
                    <div class="processQueue">
                        {os.blockedProcesses.processes.map((p, pi) => (
                            <ProcessComp pid={p.pid} name={p.name} state={p.state} priority={p.priority} timeRan={p.time_ran} timeToRun={p.time_to_run} />
                        )
                        )}
                    </div>
                ) : (
                    <p>Empty</p>
                )}
            </div>


        </div>
    )
}

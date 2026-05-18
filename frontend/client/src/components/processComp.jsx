
export default function ProcessComp({pid, name, state, priority, timeRan, timeToRun}){

    return(
        <div id="process" class="component">

            <h1>{name} ({pid})</h1>
            <h2>State: {state}, Priority: {priority}</h2>
            <p>{timeRan}/{timeToRun}</p>

        </div>
    )
}

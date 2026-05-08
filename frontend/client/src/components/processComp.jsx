
export default function ProcessComp({pid, name, state, priority, timeRan, timeToRun}){

    return(
        <div id="process" class="component">

            <p>{name} ({pid})</p>
            <p>State: {state}, Priority: {priority}</p>
            <p>{timeRan}/{timeToRun}</p>

        </div>
    )
}

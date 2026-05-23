
let colourMap = ['red_process', 'orange_process', 'yellow_process', 'green_process', 'blue_process', 'purple_process', 'pink_process']


export default function ProcessComp({pid, name, state, priority, timeRan, timeToRun}){
    let colour = colourMap[ Number(pid) % colourMap.length ]

    return(
        <div class={"process component " + colour}>

            <h1>{name} ({pid})</h1>
            <h2>State: {state}, Priority: {priority}</h2>
            <p>{timeRan}/{timeToRun}</p>

        </div>
    )
}

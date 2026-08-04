import { useEffect, useRef, useState, type MouseEvent as ReactMouseEvent, type PointerEvent as ReactPointerEvent } from "react"
import type { Star } from "./Star"
import "./starmap.scss"
import type { Empire } from "./empire";

export default function Starmap(props: { setSelectedStar: (star: Star | null) => void; empires: Empire[]; selectedStar?: Star | null }) {
    const [starmap, setStarmap] = useState<Star[]>([])
    const [viewOffset, setViewOffset] = useState({ x: 0, y: 0 })
    const [isDragging, setIsDragging] = useState(false)
    const [zoomLevel, setZoomLevel] = useState(1)
    const coordinateScale = 10
    const dragStartRef = useRef<{ x: number; y: number; offsetX: number; offsetY: number } | null>(null)
    const isDraggingRef = useRef(false)
    const wasDraggedRef = useRef(false)
    const containerRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        fetch("http://127.0.0.1:5000/starmap")
            .then((response) => response.json())
            .then((data) => setStarmap(data))
            .catch((error) => console.error("Error fetching starmap:", error))
    }, [])

    // Center the view on the selected star when it changes.
    useEffect(() => {
        const star = props.selectedStar
        if (!star || !containerRef.current) return

        const rect = containerRef.current.getBoundingClientRect()
        const starX = star.coordinates[0]
        const starY = star.coordinates[1]

        const centerScreenX = rect.width / 2
        const centerScreenY = rect.height / 2

        const nextViewX = centerScreenX / (zoomLevel * coordinateScale) - starX
        const nextViewY = centerScreenY / (zoomLevel * coordinateScale) - starY

        setViewOffset({ x: nextViewX, y: nextViewY })
    }, [props.selectedStar, zoomLevel])

    const handlePointerDown = (event: ReactPointerEvent<HTMLDivElement>) => {
        dragStartRef.current = {
            x: event.clientX,
            y: event.clientY,
            offsetX: viewOffset.x,
            offsetY: viewOffset.y,
        }
        isDraggingRef.current = false
        wasDraggedRef.current = false
        setIsDragging(false)
    }

    const handlePointerMove = (event: ReactPointerEvent<HTMLDivElement>) => {
        if (!dragStartRef.current) {
            return
        }

        const deltaX = event.clientX - dragStartRef.current.x
        const deltaY = event.clientY - dragStartRef.current.y
        const movementThreshold = 8

        if (!isDraggingRef.current && (Math.abs(deltaX) > movementThreshold || Math.abs(deltaY) > movementThreshold)) {
            isDraggingRef.current = true
            wasDraggedRef.current = true
            setIsDragging(true)
            event.currentTarget.setPointerCapture(event.pointerId)
        }

        if (!isDraggingRef.current) {
            return
        }

        setViewOffset({
            x: dragStartRef.current.offsetX + deltaX / (zoomLevel * coordinateScale),
            y: dragStartRef.current.offsetY + deltaY / (zoomLevel * coordinateScale),
        })
    }

    const handlePointerUp = (event: ReactPointerEvent<HTMLDivElement>) => {
        if (event.currentTarget.hasPointerCapture(event.pointerId)) {
            event.currentTarget.releasePointerCapture(event.pointerId)
        }

        dragStartRef.current = null
        isDraggingRef.current = false
        setIsDragging(false)
    }


    const handleScroll = (event: React.WheelEvent<HTMLDivElement>) => {
        const rect = event.currentTarget.getBoundingClientRect()
        const mouseX = event.clientX - rect.left
        const mouseY = event.clientY - rect.top
        const zoomFactor = 0.1
        const nextZoomLevel = Math.max(0.1, Math.min(zoomLevel - event.deltaY * zoomFactor * 0.01, 10))

        if (nextZoomLevel === zoomLevel) {
            return
        }

        const worldX = mouseX / (zoomLevel * coordinateScale) - viewOffset.x
        const worldY = mouseY / (zoomLevel * coordinateScale) - viewOffset.y

        setViewOffset({
            x: mouseX / (nextZoomLevel * coordinateScale) - worldX,
            y: mouseY / (nextZoomLevel * coordinateScale) - worldY,
        })
        setZoomLevel(nextZoomLevel)
    }

    const handleStarClick = (event: ReactMouseEvent<HTMLDivElement>, star: Star) => {
        event.stopPropagation()
        props.setSelectedStar(star)
    }

    const isStarInteractionTarget = (target: EventTarget | null) => {
        if (!(target instanceof HTMLElement)) {
            return false
        }

        return target.closest(".star, .star-container, .star-background, .star-name") !== null
    }

    const handleBackgroundClick = (event: ReactMouseEvent<HTMLDivElement>) => {
        if (wasDraggedRef.current) {
            wasDraggedRef.current = false
            return
        }

        if (isStarInteractionTarget(event.target)) {
            return
        }

        props.setSelectedStar(null)
    }

    const planets_to_colors: Record<string, string> = {}
    for(let empire of props.empires) {
        for(let planet of empire.planets) {
            planets_to_colors[planet] = empire.color
        }   
    }

    return (
        <div
            className={`starmap ${isDragging ? "dragging" : ""}`}
            ref={containerRef}
            onPointerDown={handlePointerDown}
            onPointerMove={handlePointerMove}
            onPointerUp={handlePointerUp}
            onPointerCancel={handlePointerUp}
            onLostPointerCapture={handlePointerUp}
            onWheel={handleScroll}
            onClick={handleBackgroundClick}
        >
            {starmap.map((star, index) => {
                const starColor = star.planets
                    .map((planet) => planets_to_colors[planet])
                    .find((color) => Boolean(color)) ?? "white";

                return (
                    <div key={index} className="star" style={
                        {
                            left: `${(star.coordinates[0] + viewOffset.x) * zoomLevel * coordinateScale}px`,
                            top: `${(star.coordinates[1] + viewOffset.y) * zoomLevel * coordinateScale}px`,
                            color: starColor,
                        }
                    }>
                        <div className="star-container" onClick={(event) => handleStarClick(event, star)}>
                            <div className="star-background"></div>
                            <h3 className="star-name">{star.name}</h3>
                        </div>
                    </div>
                )
            })}
            {starmap.map((star, index) => (
                star.star_lane_connections.map((connectedStar, connectionIndex) => {
                    const connectedStarData = starmap.find(s => s.name === connectedStar)
                    if (!connectedStarData) return null

                    const x1 = (star.coordinates[0] + viewOffset.x) * zoomLevel * coordinateScale
                    const y1 = (star.coordinates[1] + viewOffset.y) * zoomLevel * coordinateScale - 17
                    const x2 = (connectedStarData.coordinates[0] + viewOffset.x) * zoomLevel * coordinateScale
                    const y2 = (connectedStarData.coordinates[1] + viewOffset.y) * zoomLevel * coordinateScale - 17

                    return (
                        <svg key={`${index}-${connectionIndex}`} className="star-connection" style={{ position: "absolute", left: 0, top: 0, width: "100%", height: "100%" }}>
                            <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="white" strokeWidth="1" />
                        </svg>
                    )
                })
            ))}
        </div>
    )
}
import {
  Box,
  Button,
  HStack,
  Text,
  Tooltip,
  useColorModeValue as mode,
} from '@chakra-ui/react';
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import gsap from 'gsap';

/* ---------------- types ---------------- */
export type Row = {
  id: string | number;
  vessel_name: string;
  optimizer_berth_id: string;
  arrival: string;
  optimizer_start: string;
  optimizer_end: string;
};
interface Props { calls: Row[]; playMs?: number; }

/* -------------- helpers --------------- */
const toDate = (s?: string) =>
  s ? new Date(s.replace(/(\.\d{3})\d+/, '$1')) : new Date(NaN);

const colourFor: Record<string,string> = {
  CONTAINER : '#1d4ed8',
  BULK      : '#ca8a04',
  RORO      : '#7c3aed',
  TANKER    : '#dc2626',
  OTHER     : '#4b5563',
};

/* flattened boat SVG (16×16 view-box) */
const BoatSVG = ({ fill }: { fill: string }) => (
  <svg width={36} height={36} viewBox="0 0 16 16" fill="none">
    <path d="M2 8h12l-1 4H3L2 8Z" fill={fill}/>
    <path d="M1 12h14v2H1z" fill={mode('skyblue','#0f172a')}/>
    <rect x={5} y={4} width={6} height={3} fill={fill}/>
    <rect x={6} y={2} width={4} height={2} fill={fill}/>
  </svg>
);

/* -------------- component ------------- */
export default function BoatStageTop({ calls, playMs = 60_000 }: Props) {
  const stage      = useRef<HTMLDivElement>(null);
  const tlRef      = useRef<gsap.core.Timeline | null>(null);
  const [w,setW]   = useState(0);
  const [h,setH]   = useState(0);
  const [speed,setSpeed]     = useState(1);
  const [queueIds,setQueue]  = useState<string[]>([]);
  const [clock,setClock]     = useState<Date|null>(null);

  /* size */
  useLayoutEffect(()=>{
    if(!stage.current) return;
    const ro=new ResizeObserver(e=>{
      setW(e[0].contentRect.width);
      setH(e[0].contentRect.height);
    });
    ro.observe(stage.current);
    return()=>ro.disconnect();
  },[]);

  /* data */
  const rows=useMemo<Row[]>(()=>{
    const seen=new Set<string>();
    return calls.filter(r=>!seen.has(String(r.id)) && seen.add(String(r.id)))
      .map(r=>({...r,id:String(r.id)}))
      .sort((a,b)=>toDate(a.arrival).getTime()-toDate(b.arrival).getTime());
  },[calls]);

  const berths=useMemo(
    ()=>[...new Set(rows.map(r=>r.optimizer_berth_id))].sort(),[rows]);

  /* build TL */
  useEffect(()=>{
    if(!rows.length||!w||!h) return;
    tlRef.current?.kill();
    const tl=gsap.timeline(); tlRef.current=tl;

    const t0=toDate(rows[0].arrival).getTime();
    const span=toDate(rows.at(-1)!.optimizer_end).getTime()-t0;
    const msPerTl=span/(playMs/1000); tl.data={t0,msPerTl};

    setClock(new Date(t0));
    setQueue(rows.map(r=>r.id as string));

    const slotW=w/berths.length;
    const slotX=(b:string)=>berths.indexOf(b)*slotW+slotW/2-18;
    const offX=-60, offY=h+60;

    rows.forEach((r,i)=>{
      const tArr=(toDate(r.arrival).getTime()-t0)/msPerTl;
      const tEta=(toDate(r.optimizer_start).getTime()-t0)/msPerTl;
      const tEnd=(toDate(r.optimizer_end).getTime()-t0)/msPerTl;
      const sel=`[data-ship="${r.id}"]`;

      tl.fromTo(sel,{x:offX,y:offY,opacity:0},
        {x:80,y:h-60-i*48,opacity:1,duration:1,ease:'power1.out'},tArr);

      tl.to(sel,{
        x:slotX(r.optimizer_berth_id),y:48,duration:1,ease:'power1.inOut',
        onStart:()=>setQueue(q=>q.filter(id=>id!==r.id)),
        attr:{'data-docked':'y'},
      },tEta);

      tl.to(sel,{
        y:offY,duration:1,ease:'power1.in',
        attr:{'data-docked':null},
      },tEnd);
    });

    const tick=()=>{
      const d=tl.data as{t0:number;msPerTl:number};
      setClock(new Date(d.t0+tl.rawTime()*d.msPerTl));
    };
    gsap.ticker.add(tick); tl.eventCallback('onComplete',()=>gsap.ticker.remove(tick));
    return()=>{gsap.ticker.remove(tick);tl.kill();};
  },[rows,w,h,playMs,berths]);

  useEffect(()=>{tlRef.current?.timeScale(speed);},[speed]);

  useEffect(()=>{
    queueIds.forEach((id,idx)=>{
      gsap.to(`[data-ship="${id}"]`,
        {y:h-60-idx*48,duration:0.4,ease:'power1.out'});
    });
  },[queueIds,h]);

  /* styles */
  const waterGrad = `repeating-linear-gradient(
     0deg, ${mode('#e0f2fe','#1e3a8a')} 0 5px,
           ${mode('#dbeafe','#172554')} 5px 10px)`;
  return(
    <Box ref={stage} pos="relative" w="100%" h="540px"
         bg={waterGrad} overflow="hidden">

      {/* waves animation */}
      <Box pos="absolute" inset={0}
           bg={`url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjEwIiBmaWxsPSIjMDAwMCIgZmlsbC1vcGFjaXR5PSIwLjAzIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMTAiIHk9IjAiIC8+PC9zdmc+")`}
           bgSize="300px 10px" bgRepeat="repeat-x"
           animation="wave 6s linear infinite"
           pointerEvents="none"
      />
      <style>
        {`@keyframes wave{from{background-position-x:0}to{background-position-x:-300px}}`}
      </style>

    
      {berths.map((b,i)=>(
        <Box key={b} pos="absolute" top="0"
             left={`${i*(100/berths.length)}%`}
             w={`${100/berths.length}%`} h="40px"
             bg={mode('#9ca3af','#4b5563')}
             bgImage="url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNC
              IgaGVpZ2h0PSI0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRo
              PSI0IiBoZWlnaHQ9IjQiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNiIgLz48L3N2Zz4=')"
             bgSize="4px 4px"
             borderRight="1px solid rgba(0,0,0,.15)">
          <Box pos="absolute" top="28px" left="50%" w="4px" h="8px"
               bg="yellow.500" borderRadius="2px" transform="translateX(-50%)"/>
          <Text textAlign="center" fontSize="sm" pt="10px" fontWeight="bold">{b}</Text>
        </Box>
      ))}

      {/* queue rope */}
      <Box pos="absolute" left="64px" bottom="8px" h={`${Math.min(queueIds.length,5)*48}px`}
           borderLeft="2px dashed rgba(255,255,255,.5)" />

      {/* HUD */}
      <HStack pos="absolute" top="6px" right="14px" spacing={2} zIndex={50}
              p="6px 10px" borderRadius="20px" backdropFilter="blur(6px)"
              bg={mode('rgba(255,255,255,.6)','rgba(0,0,0,.35)')} >
        <Button size="xs" variant="ghost" onClick={()=>setSpeed(s=>Math.max(.5,s-.5))}>−</Button>
        <Text fontSize="sm" fontWeight="bold" w="30px" textAlign="center">{speed.toFixed(1)}×</Text>
        <Button size="xs" variant="ghost" onClick={()=>setSpeed(s=>Math.min(5,s+.5))}>+</Button>
        <Text fontSize="sm" fontFamily="mono">
          {clock?clock.toISOString().substring(11,16):'--:--'}
        </Text>
      </HStack>

      {/* ships */}
      {rows.map(r=>{
        const eta=toDate(r.optimizer_start).toISOString().substring(11,16);
        const etd=toDate(r.optimizer_end).toISOString().substring(11,16);
        return (
          <Tooltip key={r.id}
                   label={`${r.vessel_name}\nETB ${eta} – ETD ${etd}`}
                   bg="gray.700" color="white" borderRadius="md" p={2}
                   whiteSpace="pre" fontSize="xs">
            <Box data-ship={r.id} pos="absolute"
                 transform="translate(-50%,-50%)"
                 filter="drop-shadow(1px 1px 2px #0006)"
                 _hover={{transform:'translate(-50%,-50%) scale(1.18)'}}>
              <BoatSVG fill={colourFor[r.vessel_type]??colourFor.OTHER}/>
            </Box>
          </Tooltip>
        );
      })}
    </Box>
  );
}

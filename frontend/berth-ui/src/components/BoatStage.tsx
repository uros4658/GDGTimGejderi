import { useEffect, useMemo, useRef } from 'react';
import { motion, useAnimationControls } from 'framer-motion';
import { Box, Text } from '@chakra-ui/react';

type RowFlat = {
  id: string | number;
  vessel_name: string;
  vessel_type: string;
  optimizer_berth_id: string;
  optimizer_start: string;
  optimizer_end: string;
};
interface Props { calls: RowFlat[]; playMs?: number; }

const COLORS: Record<string,string> = {
  CONTAINER:'#0364e6', RORO:'#6b21a8', BULK:'#d97706',
  TANKER:'#dc2626', OTHER:'#64748b',
};

export default function BoatStage({ calls, playMs = 60_000 }: Props) {
  const ctrl   = useAnimationControls();
  const timers = useRef<number[]>([]);

  /* -------- normalise rows -------- */
  const timeline = useMemo(() => {
    const seen = new Set<string>();
    return calls
      .filter(r => !seen.has(String(r.id)) && seen.add(String(r.id)))
      .map(r => ({
        id:   String(r.id),
        name: r.vessel_name,
        type: r.vessel_type ?? 'OTHER',
        berth:r.optimizer_berth_id,
        eta:  r.optimizer_start,
        etd:  r.optimizer_end,
      }))
      .sort((a,b)=>new Date(a.eta).getTime()-new Date(b.eta).getTime());
  }, [calls]);

  if (!timeline.length) return null;

  const t0=new Date(timeline[0].eta).getTime();
  const tEnd=new Date(timeline.at(-1)!.etd).getTime();
  const scale=playMs/Math.max(1,tEnd-t0);

  /* -------- schedule once per change -------- */
  useEffect(()=>{
    timers.current.forEach(clearTimeout);
    timers.current=[];             // reset
    ctrl.set(()=>({left:'110%'})); // docked off-screen

    console.log('[BoatStage] rows',timeline.length,' playMs',playMs);

    timeline.forEach(c=>{
      const eta=new Date(c.eta).getTime();
      const etd=new Date(c.etd).getTime();
      const delay=(eta-t0)*scale;
      const stay =(etd-eta)*scale;

      console.log('→ schedule',c.name,'delay',delay.toFixed(0));
      timers.current.push(
        window.setTimeout(()=>{
          console.log('🛳 dock ',c.name);
          ctrl.start(i=>i===c.id?{left:8,transition:{duration:1}}:{});

          timers.current.push(
            window.setTimeout(()=>{
              console.log('🛳 leave',c.name);
              ctrl.start(i=>i===c.id?{left:'-120%',transition:{duration:1}}:{});
            },stay)
          );
        },delay)
      );
    });

    return()=>timers.current.forEach(clearTimeout);
  },[timeline,timeline.length,t0,scale,playMs]);   // ← fixed-length list

  /* -------- layout -------- */
  const berths=[...new Set(timeline.map(c=>c.berth))].sort().reverse();
  const laneY=(b:string)=>`${20+berths.indexOf(b)*80}px`;

  return(
    <Box pos="relative" w="100%"
      border="2px dashed red"
     overflow="visible"
         h={`${berths.length*80+40}px`} bg="blue.50" overflow="hidden">
      <Box pos="absolute" left={0} top={0} bottom={0} w="8px" bg="gray.700"/>
      {timeline.map(c=>(
        <motion.div
         data-id={c.id}
          key={`${c.id}-${c.berth}`}
          custom={c.id}
          animate={ctrl}
          initial={{left:'110%',top:laneY(c.berth)}}
          style={{
            position:'absolute',width:110,height:28,
            background:COLORS[c.type]??COLORS.OTHER,borderRadius:4,
            display:'flex',flexDirection:'column',alignItems:'center',
            justifyContent:'center',color:'#fff',fontSize:10,zIndex:5
          }}>
          <Text>{c.name}</Text>
          <Text fontSize="8px">{c.berth}</Text>
        </motion.div>
      ))}
    </Box>
  );
}

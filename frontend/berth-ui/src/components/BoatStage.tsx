// BoatStageTop.tsx
import {
  Box, Button, HStack, Text, Tooltip, useColorModeValue as mode,
} from '@chakra-ui/react';
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import gsap from 'gsap';

/* ---------- types ---------- */
export type Row = {
  id: string | number;
  vessel_name: string;
  vessel_type?: string;
  optimizer_berth_id: string;
  arrival: string;           // ISO – physical arrival at anchorage
  optimizer_start: string;   // ETB
  optimizer_end: string;     // ETD
};
interface Props {
  calls: Row[];
  playMs?: number;
}

/* ---------- helpers ---------- */
const toDate = (s?: string) =>
  s ? new Date(s.replace(/(\.\d{3})\d+/, "$1")) : new Date(NaN);

const colourFor: Record<string, string> = {
  CONTAINER: '#1d4ed8',
  BULK     : '#ca8a04',
  RORO     : '#7c3aed',
  TANKER   : '#dc2626',
  OTHER    : '#4b5563',
};

/* tiny 36×36 boat svg */
const BoatSVG = ({ fill }: { fill: string }) => (
  <svg width={36} height={36} viewBox="0 0 16 16" fill="none">
    <path d="M2 8h12l-1 4H3L2 8Z"           fill={fill}/>
    <path d="M1 12h14v2H1z"                 fill={mode('#bae6fd', '#0f172a')}/>
    <rect x={5} y={4} width={6} height={3} fill={fill}/>
    <rect x={6} y={2} width={4} height={2} fill={fill}/>
  </svg>
);

/* ---------- component ---------- */
export default function BoatStageTop({ calls, playMs = 60_000 }: Props) {
  const stageRef               = useRef<HTMLDivElement>(null);
  const tlRef                  = useRef<gsap.core.Timeline | null>(null);
  const [width,  setWidth]     = useState(0);
  const [height, setHeight]    = useState(0);
  const [speed,  setSpeed]     = useState(1);
  const [queueIds, setQueue]   = useState<string[]>([]);
  const [clock, setClock]      = useState<Date | null>(null);

  /* stage size ----------------------------------------------------------- */
  useLayoutEffect(() => {
    if (!stageRef.current) return;
    const ro = new ResizeObserver(([e]) => {
      setWidth(e.contentRect.width);
      setHeight(e.contentRect.height);
    });
    ro.observe(stageRef.current);
    return () => ro.disconnect();
  }, []);

  /* normalised / sorted rows -------------------------------------------- */
  const rows = useMemo<Row[]>(() => {
    const seen = new Set<string>();
    return calls
      .filter(r => !seen.has(String(r.id)) && seen.add(String(r.id)))
      .map(r => ({ ...r, id: String(r.id) }))
      .sort((a, b) => toDate(a.arrival).getTime() - toDate(b.arrival).getTime());
  }, [calls]);

  const berths = useMemo(
    () => [...new Set(rows.map(r => r.optimizer_berth_id))].sort(),
    [rows]
  );

  /* build GSAP timeline -------------------------------------------------- */
  useEffect(() => {
    if (!rows.length || !width || !height) return;

    tlRef.current?.kill();
    const tl = gsap.timeline({ defaults: { ease: 'none' } });
    tlRef.current = tl;

    const t0 = toDate(rows[0].arrival).getTime();  // first arrival
    const msPerTl = playMs;                        // schedule-ms per TL-sec
    tl.data = { t0, msPerTl };

    /* geometry helpers */
    const slotW  = width / berths.length;
    const slotX  = (b: string) => berths.indexOf(b) * slotW + slotW / 2;
    const slotY  = 80;                             // berth lane Y
    const anchor = { x: 80, y: height - 60 };      // queue start (bottom-left)

    setClock(new Date(t0));
    setQueue(rows.map(r => String(r.id)));         // all start in queue

    rows.forEach((r, idx) => {
      const idSel = `[data-ship="${r.id}"]`;

      /* absolute times converted to TL seconds */
      const tArrive = (toDate(r.arrival).getTime()        - t0) / msPerTl;
      const tBerth  = (toDate(r.optimizer_start).getTime() - t0) / msPerTl;
      const tLeave  = (toDate(r.optimizer_end).getTime()   - t0) / msPerTl;

      /* initial queue position – stack upwards */
      tl.set(idSel, {
        x: anchor.x, y: anchor.y - idx * 48, autoAlpha: 0,
      });

      /* show on physical arrival */
      tl.to(idSel, { autoAlpha: 1, duration: 0.2 }, tArrive);

      /* sail to berth */
      tl.to(idSel,
        {
          x: slotX(r.optimizer_berth_id),
          y: slotY,
          duration: tBerth - tArrive,
          ease: 'power1.inOut',
          onStart: () =>
            setQueue(q => q.filter(qid => qid !== String(r.id))),
        },
        tArrive
      );

      /* leave berth + sail right out of frame */
      tl.to(idSel,
        {
          x: width + 100,
          y: slotY,
          duration: 1,
          ease: 'power1.in',
        },
        tLeave
      );
    });

    /* clock tick -------------------------------------------------------- */
    const tick = () => {
      const { t0: start, msPerTl: scale } =
        tl.data as { t0: number; msPerTl: number };
      setClock(new Date(start + tl.rawTime() * scale));
    };
    gsap.ticker.add(tick);
    tl.eventCallback('onComplete', () => gsap.ticker.remove(tick));

    return () => {
      gsap.ticker.remove(tick);
      tl.kill();
    };
  }, [rows, width, height, playMs, berths]);

  /* speed scale ---------------------------------------------------------- */
  useEffect(() => { tlRef.current?.timeScale(speed); }, [speed]);

  /* re-stack remaining queue when one departs --------------------------- */
  useEffect(() => {
    queueIds.forEach((id, i) => {
      gsap.to(`[data-ship="${id}"]`, {
        y: height - 60 - i * 48,
        duration: 0.4,
        ease: 'power1.out',
      });
    });
  }, [queueIds, height]);

  /* ------------------------ render ------------------------------------- */
  const waterGrad = `repeating-linear-gradient(
     0deg, ${mode('#e0f2fe', '#1e3a8a')} 0 5px,
           ${mode('#dbeafe', '#172554')} 5px 10px)`;

  return (
    <Box ref={stageRef} pos="relative" w="100%" h="540px"
         bg={waterGrad} overflow="hidden">

      {/* berth strip */}
      {berths.map((b, i) => (
        <Box key={b}
             pos="absolute"
             top="0"
             left={`${i * (100 / berths.length)}%`}
             w={`${100 / berths.length}%`}
             h="40px"
             bg={mode('#cbd5e1', '#475569')}
             borderRight="1px solid rgba(0,0,0,.15)">
          <Text textAlign="center" fontSize="sm" fontWeight="bold" pt="9px">
            {b}
          </Text>
        </Box>
      ))}

      {/* queue rope */}
      <Box pos="absolute"
           left="64px"
           bottom="8px"
           h={`${Math.max(queueIds.length - 1, 0) * 48}px`}
           borderLeft="2px dashed rgba(255,255,255,.6)" />

      {/* HUD */}
      <HStack pos="absolute" top="6px" right="14px" spacing={2} zIndex={100}
              p="6px 10px" borderRadius="18px"
              backdropFilter="blur(6px)"
              bg={mode('rgba(255,255,255,.65)', 'rgba(0,0,0,.45)')}>
        <Button size="xs" variant="ghost"
                onClick={() => setSpeed(s => Math.max(0.5, s - 0.5))}>−</Button>
        <Text fontSize="sm" fontWeight="semibold" w="30px" textAlign="center">
          {speed.toFixed(1)}×
        </Text>
        <Button size="xs" variant="ghost"
                onClick={() => setSpeed(s => Math.min(5, s + 0.5))}>+</Button>
        <Text fontSize="sm" fontFamily="mono">
          {clock ? clock.toISOString().substring(11, 16) : '--:--'}
        </Text>
      </HStack>

      {/* ships */}
      {rows.map(r => (
        <Tooltip key={r.id}
                 label={`${r.vessel_name}
ETB ${toDate(r.optimizer_start).toISOString().substring(11,16)}
ETD ${toDate(r.optimizer_end).toISOString().substring(11,16)}`}
                 whiteSpace="pre"
                 bg="gray.700"
                 color="white"
                 borderRadius="md"
                 p={2}
                 fontSize="xs">
          <Box data-ship={r.id}
               pos="absolute"
               transform="translate(-50%,-50%)"
               filter="drop-shadow(1px 1px 2px #0006)"
               _hover={{ transform: 'translate(-50%,-50%) scale(1.16)' }}>
            <BoatSVG fill={colourFor[r.vessel_type ?? 'OTHER']} />
          </Box>
        </Tooltip>
      ))}
    </Box>
  );
}

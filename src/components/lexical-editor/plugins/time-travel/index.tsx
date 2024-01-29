import { useAtom, useAtomValue } from "jotai";

import {
  blockThresholdInSecAtom,
  MIN_THRESHOLD_IN_SEC,
  timeTravelStateAtom,
} from "@/atoms/time-travel-atom";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import Recorder from "./components/recorder";
import Replayer from "./components/replayer";

export default function TimeTravelPlugin() {
  const timeTravelState = useAtomValue(timeTravelStateAtom);
  const [blockThresholdInSec, setBlockThresholdInSec] = useAtom(
    blockThresholdInSecAtom
  );
  return (
    <Card className="w-[400px] absolute bottom-0 left-0 z-20 m-5">
      <CardHeader>
        <CardTitle>Time Travel</CardTitle>
        <CardDescription>
          Record and replay your writing sessions.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex justify-between items-center space-x-2">
        {
          {
            recording: <Recorder />,
            replaying: <Replayer />,
          }[timeTravelState]
        }
      </CardContent>
      {timeTravelState === "replaying" && (
        <CardFooter>
          <div className="flex flex-col space-y-2 w-full">
            <Label htmlFor="blockThresholdInSec">
              Block Threshold (in sec)
            </Label>
            <Input
              id="blockThresholdInSec"
              type="number"
              min={MIN_THRESHOLD_IN_SEC}
              placeholder="Block Threshold"
              value={blockThresholdInSec}
              onChange={(e) => {
                setBlockThresholdInSec(Number(e.target.value));
              }}
            />
          </div>
        </CardFooter>
      )}
    </Card>
  );
}

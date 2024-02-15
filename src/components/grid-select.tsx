import { SetStateAction, useAtom, WritableAtom } from "jotai";

import { Label } from "@/components/ui/label";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { InfoCircledIcon } from "@radix-ui/react-icons";

import { Button } from "./ui/button";
import { ToggleGroup, ToggleGroupItem } from "./ui/toggle-group";

export interface GridSelectProps {
  label?: string;
  tooltip?: string;
  atom: WritableAtom<number, [SetStateAction<number>], void>;
}

export default function GridSelect({ label, tooltip, atom }: GridSelectProps) {
  const [value, setValue] = useAtom(atom);
  return (
    <div className="flex flex-col space-y-3">
      {label && (
        <TooltipProvider>
          <div className="flex flex-row items-center">
            <Label>{label}</Label>
            {!!tooltip && (
              <Tooltip delayDuration={100}>
                <TooltipTrigger asChild>
                  <Button size={"icon"} variant={"link"}>
                    <InfoCircledIcon className="w-4 h-4" />
                  </Button>
                </TooltipTrigger>

                <TooltipContent>{tooltip}</TooltipContent>
              </Tooltip>
            )}
          </div>
        </TooltipProvider>
      )}

      <div className="space-y-1">
        <ToggleGroup
          type="single"
          variant="outline"
          size={"sm"}
          value={value ? value.toString() : ""}
          onValueChange={(value) => {
            setValue(parseInt(value));
          }}
        >
          {[1, 2, 3, 4, 5].map((option, index) => (
            <ToggleGroupItem key={index} value={option.toString()}>
              {option}
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
        <div className="flex flex-row justify-between">
          <Label className="text-xs text-muted-foreground">
            Highly unlikely
          </Label>
          <Label className="text-xs text-muted-foreground">Highly likely</Label>
        </div>
      </div>
    </div>
  );
}

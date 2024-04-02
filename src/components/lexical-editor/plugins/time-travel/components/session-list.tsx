import { useAtom, useSetAtom } from "jotai";
import { toast } from "sonner";
import { v4 as uuidv4 } from "uuid";

import {
  currentSessionIdAtom,
  latestEditorStateAtom,
  Session,
  sessionListAtom,
  timeTravelStateAtom,
} from "@/atoms/time-travel-atom";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { downloadFile, openFileDialog } from "@/lib/file";
import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import {
  Cross2Icon,
  DownloadIcon,
  PlayIcon,
  UploadIcon,
} from "@radix-ui/react-icons";

export default function SessionList() {
  const [editor] = useLexicalComposerContext();
  const [sessionList, setSessionList] = useAtom(sessionListAtom);
  const setLatestEditorState = useSetAtom(latestEditorStateAtom);

  // const [timeTravelLogList, setTimeTravelLogList] = useAtom(
  //   timeTravelLogListAtom
  // );

  const onDownloadLog = async (id: string, detail: boolean = true) => {
    // const res = await fetch(`/api/time-travel/${id}`, {
    //   method: "GET",
    // });

    const session = sessionList.find((log) => log.id === id);

    if (!session) {
      return;
    }

    const date = new Date(session.save_time);
    const dateString = `${date.getFullYear()}-${
      date.getMonth() + 1
    }-${date.getDate()}`;

    if (detail) {
      downloadFile(
        JSON.stringify(session),
        `watom-session-${dateString}-${session.save_time.getTime()}-${id}.json`
      );
    } else {
      const preciseLog = {
        written_text: session.written_text,
        blocks: session.blocks.filter((block) => block.annotated === true),
      };
      downloadFile(
        JSON.stringify(preciseLog),
        `watom-log-${dateString}-${session.save_time.getTime()}-${id}-precise.json`
      );
    }

    // const blob = new Blob([JSON.stringify(log)], {
    //   type: "application/json",
    // });

    // const url = URL.createObjectURL(blob);

    // // save the file
    // const link = document.createElement("a");
    // link.href = url;
    // link.download = `time-travel-log-${id}.json`;
    // link.click();
  };

  const setTimeTravelState = useSetAtom(timeTravelStateAtom);

  const setCurrentSessionId = useSetAtom(currentSessionIdAtom);

  // const router = useRouter();

  return (
    <div className="flex flex-col space-y-2 w-full">
      <div className="flex flex-row justify-between items-center">
        <Label>Pre-recorded logs</Label>
        <Button
          variant={"ghost"}
          size={"icon"}
          className="ml-auto"
          onClick={async () => {
            const data = await openFileDialog();

            try {
              const session = JSON.parse(data) as Session;

              session.id = uuidv4();
              session.save_time = new Date();
              session.logs = session.logs.map((log) => ({
                ...log,
                editorState: editor.parseEditorState(log.editorState),
              }));

              setSessionList([...sessionList, session]);

              toast.success("Log imported successfully.");
            } catch (error) {
              toast.error("Invalid log file, please try again." + error);
            }
          }}
        >
          <UploadIcon />
        </Button>
      </div>
      {sessionList.length === 0 ? (
        <div className="text-center text-muted-foreground text-sm">
          No logs yet.
        </div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Save Time</TableHead>
              <TableHead>Length</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sessionList.map((session, index) => (
              <TableRow key={index}>
                <TableCell>
                  {new Date(session.save_time).toLocaleString()}
                </TableCell>
                <TableCell>{session.logs.length} Actions</TableCell>
                <TableCell className="flex space-x-2">
                  <Button
                    className="px-0"
                    variant={"link"}
                    onClick={() => {
                      setCurrentSessionId(session.id);
                      setLatestEditorState(editor.getEditorState());
                      setTimeTravelState("replaying");
                    }}
                  >
                    <PlayIcon className="w-4 h-4" />
                  </Button>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        className="px-0"
                        variant={"link"}
                        // onClick={async () => {
                        //   await onDownloadLog(log.id);
                        //   router.refresh();
                        // }}
                      >
                        <DownloadIcon className="w-4 h-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                      <DropdownMenuItem
                        onClick={async () => {
                          await onDownloadLog(session.id, true);
                        }}
                      >
                        Detail
                      </DropdownMenuItem>
                      <DropdownMenuItem
                        onClick={async () => {
                          await onDownloadLog(session.id, false);
                        }}
                      >
                        Block Only
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                  <Button
                    className="px-0 text-red-700"
                    // size={"icon"}
                    variant={"link"}
                    onClick={async () => {
                      // await onDeleteLog(log.id);
                      setSessionList(
                        sessionList.filter((item) => item.id !== session.id)
                      );
                      // router.refresh();
                    }}
                  >
                    <Cross2Icon className="w-4 h-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}

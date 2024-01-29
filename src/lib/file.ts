export async function openFileDialog(): Promise<string> {
  return new Promise((resolve, reject) => {
    const input = document.createElement("input");
    input.type = "file";
    input.style.display = "none";
    input.addEventListener("change", () => {
      const file = input.files?.item(0);
      if (!file) {
        reject("No file selected");
        return;
      }
      const reader = new FileReader();

      reader.readAsText(file);

      reader.addEventListener("load", () => {
        resolve(reader.result as string);
      });
    });
    input.click();
  });
}

export function downloadFile(content: string, filename: string) {
  const blob = new Blob([content], {
    type: "application/json",
  });

  const url = URL.createObjectURL(blob);

  // save the file
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
}

import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const input = "C:\\buildAI\\P-046\\database\\mvp\\outputs\\agent_dataset_20260803\\XHome_Agent_Test_Dataset.xlsx";
const qa = "C:\\buildAI\\P-046\\database\\mvp\\.tmp_dataset_csv\\qa_imported";
await fs.mkdir(qa, { recursive: true });

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const summary = await workbook.inspect({
  kind: "workbook,sheet,region",
  range: "README!A1:E17",
  maxChars: 7000,
  tableMaxRows: 20,
  tableMaxCols: 8,
});
await fs.writeFile(`${qa}\\summary.ndjson`, summary.ndjson, "utf8");

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "imported workbook formula error scan",
});
await fs.writeFile(`${qa}\\formula-errors.ndjson`, errors.ndjson, "utf8");

const renderRanges = {
  README: "A1:E17",
  Properties: "A1:W12",
  Sales: "A1:J11",
  Projects: "A1:P6",
  Assignments: "A1:D20",
  SaleBusyTimes: "A1:F21",
};
for (const [sheetName, range] of Object.entries(renderRanges)) {
  const preview = await workbook.render({ sheetName, range, scale: 0.8, format: "png" });
  await fs.writeFile(`${qa}\\${sheetName}.png`, new Uint8Array(await preview.arrayBuffer()));
}

import type { FC } from "react";

interface FileItem {
  name: string;
  size: number;
}

interface FileListProps {
  files: FileItem[];
  onRemove: (index: number) => void;
}

export const FileList: FC<FileListProps> = ({ files, onRemove }) => {
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className="mt-4 space-y-2">
      {files.map((file, index) => (
        <div
          key={index}
          className="flex items-center justify-between p-2 bg-card rounded-md border border-border"
        >
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium">{file.name}</span>
            <span className="text-sm text-muted-foreground">
              {formatFileSize(file.size)}
            </span>
          </div>
          <button
            onClick={() => onRemove(index)}
            className="text-destructive hover:text-destructive/80"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
};

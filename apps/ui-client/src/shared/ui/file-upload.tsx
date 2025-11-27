import type { FC } from "react";
import { useState, useCallback, useRef } from "react";
import { FileList } from "./file-list";

export const FileUpload: FC = () => {
  const [files, setFiles] = useState<{ name: string; size: number }[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();

    const droppedFiles = Array.from(e.dataTransfer.files).map((file) => ({
      name: file.name,
      size: file.size,
    }));

    setFiles((prev) => [...prev, ...droppedFiles]);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleRemove = useCallback((index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const handleClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFiles = Array.from(e.target.files || []).map((file) => ({
        name: file.name,
        size: file.size,
      }));

      setFiles((prev) => [...prev, ...selectedFiles]);
    },
    []
  );

  return (
    <div className="w-full">
      <input
        type="file"
        ref={fileInputRef}
        className="hidden"
        multiple
        onChange={handleFileSelect}
      />
      <div
        className="border-2 border-dashed border-border rounded-lg p-4 text-center cursor-pointer hover:border-primary transition-colors"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={handleClick}
      >
        <p className="text-muted-foreground text-sm">
          Перетащите файлы сюда или кликните для выбора
        </p>
      </div>

      {files.length > 0 && <FileList files={files} onRemove={handleRemove} />}
    </div>
  );
};

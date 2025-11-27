import type { FC } from "react";
import { useState, useCallback } from "react";
import { Input } from "./input";

interface SearchListProps {
  items?: string[];
  onSelect?: (item: string) => void;
}

const mockItems = [
  "Анализ финансовых показателей",
  "Прогноз доходности",
  "Оценка рисков",
  "Анализ рынка",
  "Финансовое планирование",
  "Бюджетирование",
  "Управление активами",
  "Инвестиционный анализ",
  "Кредитный анализ",
  "Анализ ликвидности",
  "Оценка стоимости бизнеса",
  "Финансовое моделирование",
  "Анализ денежных потоков",
  "Оценка эффективности",
  "Стратегическое планирование",
  "Анализ конкурентов",
  "Оценка инвестиционных проектов",
  "Финансовый аудит",
  "Анализ рентабельности",
  "Управление рисками",
  "Анализ финансовой устойчивости",
  "Оценка кредитоспособности",
  "Финансовый консалтинг",
  "Анализ эффективности инвестиций",
  "Оценка финансового состояния",
  "Анализ капитальных вложений",
  "Финансовый контроль",
  "Анализ прибыльности",
  "Оценка финансовых результатов",
  "Анализ финансовой отчетности",
];

export const SearchList: FC<SearchListProps> = ({
  items = mockItems,
  onSelect,
}) => {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredItems = items.filter((item) =>
    item.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSearch = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  }, []);

  const handleItemClick = useCallback(
    (item: string) => {
      onSelect?.(item);
    },
    [onSelect]
  );

  return (
    <div className="flex flex-col gap-2">
      <Input
        placeholder="Поиск..."
        value={searchQuery}
        onChange={handleSearch}
      />
      <div className="max-h-[300px] overflow-y-auto scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent hover:scrollbar-thumb-accent">
        {filteredItems.map((item, index) => (
          <div
            key={index}
            className="p-2 hover:bg-accent hover:text-accent-foreground cursor-pointer rounded-md text-sm transition-colors"
            onClick={() => handleItemClick(item)}
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
};

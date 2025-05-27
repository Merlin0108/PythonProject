from collections import Counter
import statistics

class SequenceModel:
    def __init__(self):
        self.numbers = []

    def load_from_file(self, filename):
        self.numbers.clear()
        with open(filename, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                if self._is_valid_int(line):
                    self.numbers.append(int(line))
                else:
                    # Пропускаем некорректные строки, можно добавить логирование
                    print(f"Warning: invalid data on line {line_number}: '{line}'")

    def add_number(self, num):
        if isinstance(num, int):
            self.numbers.append(num)

    def edit_number(self, index, new_num):
        if 0 <= index < len(self.numbers) and isinstance(new_num, int):
            self.numbers[index] = new_num

    def delete_number(self, index):
        if 0 <= index < len(self.numbers):
            del self.numbers[index]

    def get_frequencies(self):
        return Counter(self.numbers)

    def get_min(self):
        return min(self.numbers) if self.numbers else None

    def get_max(self):
        return max(self.numbers) if self.numbers else None

    def get_mean(self):
        return statistics.mean(self.numbers) if self.numbers else None

    def get_mode(self):
        if not self.numbers:
            return None

        frequencies = self.get_frequencies()
        max_freq = max(frequencies.values())

        modes = [num for num, freq in frequencies.items() if freq == max_freq]

        if len(modes) == 1:
            return modes[0]
        else:
            return None  # Моды нет

    def _is_valid_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

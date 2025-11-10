# collector.py
Pobiera dane indeksu z API oraz cene BTC, łączy ich na podstawie wspólnych dat i zapisuje do pliku data.csv
# charts.py
Rysuje różne wykresy, pozwalające ocenić zależność między parametrami. Wizualizuje działanie algorytmu, pokazująć przy jakiej cenie jaki sygnał daje strategia. Porównać wyniki dla różnych parametrów strategii.
# static.py
Sprawdza strategię kupna poniżej indeksu X i sprzedaży, gdy indeks jest Y lub wyżej. Przebiera różne kombinacje i pokazuje wykresy porównawcze
# sharp.py
Do powyższego podejścia dodaje wykrycie naglej zmiany indeksu (skoku). Dla wykrycia skoku śledzi Moving Average i przekroczenie progu odchylenia. Przebiera kombinacje tych czterech wartośći i pokazuje wykresy porównawcze
# labels.py
Zamiast przywiązania do wartośći indeksu bierzę uogólnione etykiety przedziałów. I przebiera kombinację kupna i sprzedaży na podstawie ich wartośći.
# backtest.py
Sprawdza strategie, symulująć targ według podanych sygnałów.
Sprawdza czy najlepsze wartości są statystycznie zyskowne czy raczej są odchyleniem od normy
# make_data.py
Stosuje jedna z trzech strategii (labels, sharp, static) do danych wykorzystując ręcznie podane parametry, aby przygotować danę do uczenia maszynowego

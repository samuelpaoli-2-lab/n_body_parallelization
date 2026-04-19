CXX = g++
CXXFLAGS = -fopenmp -O3 -march=native -ffast-math
target = prova_1_n_body

all: $(target)

$(target): $(target).cpp
	$(CXX) $(CXXFLAGS) -o $(target) $(target).cpp

test: $(target)
	@echo "--- Test con 4000 corpi, dt = 0.1 e T = 60 ---"
	OMP_SCHEDULE=dynamic OMP_NUM_THREADS=12 ./$(target) 20000 0.1 60
	@echo "Test completato!"


test_1000: $(target)
	@echo "Thread,Schedule,Run,Time" > risultati_1000.csv
	@for s in static dynamic guided; do \
		for t in 1 2 4 8 12 16 20 24 28 32; do \
			echo "Testando $$s con $$t thread..."; \
			for r in $$(seq 1 5); do \
				TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 1000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
				echo "$$t,$$s,$$r,$$TIME" >> risultati_1000.csv; \
			done \
		done \
	done

test_2000: $(target)
	@echo "Thread,Schedule,Run,Time" > risultati_2000.csv
	@for s in static dynamic guided; do \
		for t in 1 2 4 8 12 16 20 24 28 32; do \
			echo "Testando $$s con $$t thread..."; \
			for r in $$(seq 1 5); do \
				TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 2000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
				echo "$$t,$$s,$$r,$$TIME" >> risultati_2000.csv; \
			done \
		done \
	done

test_4000: $(target)
	@echo "Thread,Schedule,Run,Time" > risultati_4000.csv
	@for s in static dynamic guided; do \
		for t in 1 2 4 8 12 16 20 24 28 32; do \
			echo "Testando $$s con $$t thread..."; \
			for r in $$(seq 1 5); do \
				TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
				echo "$$t,$$s,$$r,$$TIME" >> risultati_4000.csv; \
			done \
		done \
	done

test_8000: $(target)
	@echo "Thread,Schedule,Run,Time" > risultati_8000.csv
	@for s in static dynamic guided; do \
		for t in 1 2 4 8 12 16 20 24 28 32; do \
			echo "Testando $$s con $$t thread..."; \
			for r in $$(seq 1 5); do \
				TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
				echo "$$t,$$s,$$r,$$TIME" >> risultati_8000.csv; \
			done \
		done \
	done

test_12000: $(target)
	@echo "Thread,Schedule,Run,Time" > risultati_12000.csv
	@for s in static dynamic guided; do \
		for t in 1 2 4 8 12 16 20 24 28 32; do \
			echo "Testando $$s con $$t thread..."; \
			for r in $$(seq 1 5); do \
				TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
				echo "$$t,$$s,$$r,$$TIME" >> risultati_12000.csv; \
			done \
		done \
	done

test_16000: $(target)
	@echo "Thread,Schedule,Run,Time" > risultati_16000.csv
	@for s in static dynamic guided; do \
		for t in 1 2 4 8 12 16 20 24 28 32; do \
			echo "Testando $$s con $$t thread..."; \
			for r in $$(seq 1 5); do \
				TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 16000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
				echo "$$t,$$s,$$r,$$TIME" >> risultati_16000.csv; \
			done \
		done \
	done

test_20000: $(target)
	@echo "Thread,Schedule,Run,Time" > risultati_20000.csv
	@for s in static dynamic guided; do \
		for t in 1 2 4 8 12 16 20 24 28 32; do \
			echo "Testando $$s con $$t thread..."; \
			for r in $$(seq 1 5); do \
				TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 20000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
				echo "$$t,$$s,$$r,$$TIME" >> risultati_20000.csv; \
			done \
		done \
	done

test_single_20000: $(target)
	@echo "Thread,Schedule,Time" > risultati_20000_single1.csv
	@for s in dynamic guided; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			echo "Testando $$s con $$t thread..."; \
			TIME=$$(OMP_SCHEDULE=$$s OMP_NUM_THREADS=$$t ./$(target) 20000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,$$s,$$TIME" >> risultati_20000_single1.csv; \
			sleep 240; \
		done \
	done
	
	

clean:
	rm -f $(target) *.o

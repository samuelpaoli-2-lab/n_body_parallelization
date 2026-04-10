CXX = g++
CXXFLAGS = -fopenmp -O3 -march=native -ffast-math
target = prova_1_n_body

all: $(target)

$(target): $(target).cpp
	$(CXX) $(CXXFLAGS) -o $(target) $(target).cpp

test: $(target)
	@echo "--- Test con 8000 corpi, dt = 0.1 e T = 60 ---"
	OMP_SCHEDULE=static OMP_NUM_THREADS=12 ./$(target) 8000 0.1 60
	@echo "Test completato!"

test_all_multi_1_0_sch: $(target)
	@echo "--- Test con 1000 corpi, dt = 0.1 e T = 60 ---"
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule static---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=static OMP_NUM_THREADS=$$t ./$(target) 1000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule dynamic---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=dynamic OMP_NUM_THREADS=$$t ./$(target) 1000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule guided---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=guided OMP_NUM_THREADS=$$t ./$(target) 1000 0.1 60; \
		done \
	done
	@echo "Test completati!"

test_all_multi_2_0_sch: $(target)
	@echo "--- Test con 2000 corpi, dt = 0.1 e T = 60 ---"
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule static---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=static OMP_NUM_THREADS=$$t ./$(target) 2000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule dynamic---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=dynamic OMP_NUM_THREADS=$$t ./$(target) 2000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule guided---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=guided OMP_NUM_THREADS=$$t ./$(target) 2000 0.1 60; \
		done \
	done
	@echo "Test completati!"

test_all_multi_4_0_sch: $(target)
	@echo "--- Test con 4000 corpi, dt = 0.1 e T = 60 ---"
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule static---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=static OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule dynamic---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=dynamic OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule guided---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=guided OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60; \
		done \
	done
	@echo "Test completati!"

test_all_multi_8_0_sch: $(target)
	@echo "--- Test con 8000 corpi, dt = 0.1 e T = 60 ---"
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule static---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=static OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule dynamic---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=dynamic OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule guided---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=guided OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60; \
		done \
	done
	@echo "Test completati!"

test_all_multi_12_0_sch: $(target)
	@echo "--- Test con 12000 corpi, dt = 0.1 e T = 60 ---"
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule static---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=static OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule dynamic---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=dynamic OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60; \
		done \
	done
	@for t in 1 2 4 8 12; do \
		echo "--- Esecuzione con $$t thread e schedule guided---"; \
		for i in $$(seq 1 10); do \
			OMP_SCHEDULE=guided OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60; \
		done \
	done
	@echo "Test completati!"

clean:
	rm -f $(target) *.o
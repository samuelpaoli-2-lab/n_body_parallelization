CXX = g++
CXXFLAGS = -fopenmp -O3 -march=native -ffast-math -flto
target = prova_1_n_body
SRCS = $(target).cpp force_velocity_position.cpp

all: $(target) $(target_serial)

$(target): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $(target) $(SRCS)


test_4000: $(target)
	@echo "Thread,Schedule,Time" > risultati_4000.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60 0 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_4000.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	sleep 120;
	done

test_8000: $(target)
	@echo "Thread,Schedule,Time" > risultati_8000.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60 0 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_8000.csv; \
			echo "Done ($$TIME s)"; \
			sleep 120; \
		done; \
	done

test_12000: $(target)
	@echo "Thread,Schedule,Time" > risultati_12000.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60 0 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_12000.csv; \
			echo "Done ($$TIME s)"; \
			sleep 180;
		done; \
	done

test_16000: $(target)
	@echo "Thread,Schedule,Time" > risultati_16000.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 16000 0.1 60 0 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_16000.csv; \
			echo "Done ($$TIME s)"; \
			sleep 240;
		done; \
	done

test_20000: $(target)
	@echo "Thread,Schedule,Time" > risultati_20000.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 20000 0.1 60 0 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_20000.csv; \
			echo "Done ($$TIME s)"; \
			sleep 240;
		done; \
	done

test_completo: $(target)
	@$(MAKE) test_4000
	@$(MAKE) test_8000
	@$(MAKE) test_12000
	@$(MAKE) test_16000
	@$(MAKE) test_20000


sim_4000: $(target)
	OMP_SCHEDULE=dynamic OMP_NUM_THREADS=16 ./$(target) 4000 0.1 60 1

sim_8000: $(target)
	OMP_SCHEDULE=dynamic OMP_NUM_THREADS=16 ./$(target) 8000 0.1 60 1

sim_12000: $(target)
	OMP_SCHEDULE=dynamic OMP_NUM_THREADS=16 ./$(target) 12000 0.1 60 1

sim_16000: $(target)
	OMP_SCHEDULE=dynamic OMP_NUM_THREADS=16 ./$(target) 16000 0.1 60 1

sim_20000: $(target)
	OMP_SCHEDULE=dynamic OMP_NUM_THREADS=16 ./$(target) 20000 0.1 60 1

clean:
	rm -f $(target) *.o

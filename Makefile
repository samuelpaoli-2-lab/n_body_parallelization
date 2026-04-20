CXX = g++
CXXFLAGS = -fopenmp -O3 -march=native -ffast-math
target = prova_1_n_body

all: $(target)

$(target): $(target).cpp
	$(CXX) $(CXXFLAGS) -o $(target) $(target).cpp

test: $(target)
	@echo "--- Test con 4000 corpi, dt = 0.1 e T = 60 ---"
	 sleep 240;
	OMP_SCHEDULE="dynamic,32" OMP_NUM_THREADS=12 ./$(target) 20000 0.1 60
	@echo "Test completato!"


test_1000: $(target)
	@echo "Thread,Schedule,Time" > risultati_1000_ott_fisso.csv
	@for s in static "dynamic,16" "guided,16"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 1000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_1000_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_2000: $(target)
	@echo "Thread,Schedule,Time" > risultati_2000_ott_fisso.csv
	@for s in static "dynamic,16" "guided,16"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 2000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_2000_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_4000: $(target)
	@echo "Thread,Schedule,Time" > risultati_4000_ott_fisso.csv
	@for s in static "dynamic,16" "guided,16"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_4000_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_8000: $(target)
	@echo "Thread,Schedule,Time" > risultati_8000_ott_fisso.csv
	@for s in static "dynamic,16" "guided,16"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_8000_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_12000: $(target)
	@echo "Thread,Schedule,Time" > risultati_12000_ott_fisso.csv
	@for s in static "dynamic,16" "guided,16"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_12000_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_completo: $(target)
	@$(MAKE) test_1000
	@$(MAKE) test_2000
	@$(MAKE) test_4000
	@$(MAKE) test_8000
	@$(MAKE) test_12000

test_guided:$(target)
	@echo "Thread,Schedule,Time" > risultati_guided_ott_fisso.csv
	@for s in "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 1000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_guided_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done
	
	@for s in "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 2000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_guided_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done
	
	@for s in "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_guided_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done
	
	@for s in "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_guided_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done
	
	@for s in "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256 512 1024; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_guided_ott_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done
	

clean:
	rm -f $(target) *.o

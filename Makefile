CXX = g++
CXXFLAGS = -fopenmp -O3 -march=native -ffast-math -flto
target = prova_1_n_body
SRCS = $(target).cpp force_velocity_position.cpp

all: $(target) $(target_serial)

$(target): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $(target) $(SRCS)

test: $(target)
	OMP_SCHEDULE="dynamic, 3" OMP_NUM_THREADS=16 ./$(target) 8000 0.1 60
	
	

test_4000: $(target)
	@echo "Thread,Schedule,Time" > risultati_4000_firstprivate.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 4000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_4000_fin_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_8000: $(target)
	@echo "Thread,Schedule,Time" > risultati_8000_firstprivate.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 8000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_8000_firstprivate.csv; \
			echo "Done ($$TIME s)"; \
			sleep 120; \
		done; \
	done

test_12000: $(target)
	@echo "Thread,Schedule,Time" > risultati_12000_firstprivate.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_12000_fin_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_16000: $(target)
	@echo "Thread,Schedule,Time" > risultati_16000_firstprivate.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 16000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_16000_firstprivate.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_20000: $(target)
	@echo "Thread,Schedule,Time" > risultati_20000_firstprivate.csv
	@for s in static "dynamic" "guided"; do \
		for t in 1 2 4 8 12 16 32 64 128 256; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			TIME=$$(OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 20000 0.1 60 | grep "Tempo" | awk '{print $$NF}'); \
			echo "$$t,\"$$s\",$$TIME" >> risultati_20000_fin_fisso.csv; \
			echo "Done ($$TIME s)"; \
		done; \
	done

test_completo: $(target)
	@$(MAKE) test_4000
	@$(MAKE) test_12000
	@$(MAKE) test_20000


test_private: $(target)

	@echo "Thread,Schedule,Time" > risultati_12000_ott_firstprivate.csv
	@for s in static "dynamic,16" "guided"; do \
		for t in 1 2 4 8 12; do \
			printf "Testando %-12s con %4d thread... " "$$s" "$$t"; \
			if OMP_SCHEDULE="$$s" OMP_NUM_THREADS=$$t ./$(target) 12000 0.1 60 > temp_out.txt 2>&1; then \
				TIME=$$(grep "Tempo" temp_out.txt | awk '{print $$NF}'); \
				echo "$$t,\"$$s\",$$TIME" >> risultati_12000_ott_firstprivate.csv; \
				echo "Done ($$TIME s)"; \
			else \
				echo "$$t,\"$$s\",CRASH" >> risultati_12000_ott_firstprivate.csv; \
				echo "CRASH (Segmentation Fault)"; \
			fi; \
			sleep 240; \
		done; \
	done
	@rm -f temp_out.txt




clean:
	rm -f $(target) *.o

// Computing PI using the Monte Carlo Simulation.
// Kaleb Hannan
// COS 442 HW2
// 2-4-2025

#include <pthread.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#define NumPoints 10000
#define NumThreads 4

// Globle vars
int Total_Hits = 0;
void *worker_thread(void *);
pthread_mutex_t mutex;

int main()
{
        int ret;
        int points = NumPoints/NumThreads;
        pthread_t threadID[NumThreads];
        pthread_mutex_init(&mutex,NULL);

        for(int i = 0; i < NumThreads; i++)
                {
                        ret = pthread_create(&threadID[i],NULL,worker_thread,(void*)&points);
                }
        for(int i = 0; i < NumThreads; i++)
                {
                        pthread_join(threadID[i],NULL);
                }
}
// Worker thread
void *worker_thread(void *numPointsPerThread)
{
	int numOfPoints = *(int*)numPointsPerThread;
	int numOfHits = 0;

	for(int i = 0; i < numOfPoints; i++)
		{
			// Use Monte Carlo Simulation
			
		}

	// Use Mutex to Lock Global Var
	pthread_mutex_lock(&mutex);
	Total_Hits = Total_Hits + numOfHits;
	pthread_mutex_unlock(&mutex);
}

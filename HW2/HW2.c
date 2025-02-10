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
	clock_t start, end;
        pthread_mutex_init(&mutex,NULL);

	//start timer to track time
	start = clock();

        for(int i = 0; i < NumThreads; i++)
                {
                        ret = pthread_create(&threadID[i],NULL,worker_thread,(void*)&points);
                }
        for(int i = 0; i < NumThreads; i++)
                {
                        pthread_join(threadID[i],NULL);
                }
	//calculate pi
	float pi = 4.0 * (float)Total_Hits / (float)NumPoints;
	//End Timer
	end = clock();
	double time = ((double) (end - start))/ CLOCKS_PER_SEC;
	printf("Pi == %f\n",pi);
	printf("Time == %fs\n",time);
	printf("NumHits == %d\n",Total_Hits);
}
// Worker thread
void *worker_thread(void *numPointsPerThread)
{
	int numOfPoints = *(int*)numPointsPerThread;
	int numOfHits = 0;
	unsigned int seed = time(NULL) + pthread_self();

	printf("Thread Created\n");

	for(int i = 0; i < numOfPoints; i++)
		{
			// Use Monte Carlo Simulation
			float x = ((float)rand_r(&seed)/(float)RAND_MAX) * 2.0 - 1.0;
			float y = ((float)rand_r(&seed)/(float)RAND_MAX) * 2.0 - 1.0;

			//Check to see if point is in the
			if ((x*x) + (y*y) <= 1.0)
			{
				numOfHits++;
			}
		}


	// Use Mutex to Lock Global Var
	pthread_mutex_lock(&mutex);
	Total_Hits = Total_Hits + numOfHits;
	pthread_mutex_unlock(&mutex);
}

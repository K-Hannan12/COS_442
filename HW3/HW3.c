// Computing PI using the Monte Carlo Simulation.
// Kaleb Hannan
// COS 442 HW3
// 2-16-2025

#include <pthread.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#define NumPoints 2000000000
#define NumThreads 1

// Globle vars
int Total_Hits = 0;
void *worker_thread(void *);
pthread_mutex_t mutex;

int main()
{
        int ret;
        int points = NumPoints/NumThreads;
        pthread_t threadID[NumThreads];
        struct timeval start, end;
        pthread_mutex_init(&mutex,NULL);

        //start timer to track time
        gettimeofday(&start, NULL);

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
        gettimeofday(&end, NULL);
        double time = (double)(end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1e6;
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
        //printf("new Thread Created\n");
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



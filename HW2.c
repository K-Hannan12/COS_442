// Computing PI using the Monte Carlo Simulation.
// Kaleb Hannan
// COS 442 HW2
// 2-4-2025

#include <pthread.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

// Globle vars
int Total_Hits = 0;
void worker_thread(void*);

#define NumPoints 10,000;
#define NumThreads 4;

int main()
{
	int points = NumPoints/NumThreads;
	pthread_t threadID[NumThreads];
}

// Worker thread
void *worker_thread(void *numPointsPerThread)
{
	int numOfPoints = *(int*)numPointsPerThread;
}

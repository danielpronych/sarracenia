
#include "sr_context.h"

/*
  for use by sr_post to avoid duplicate postings, sr_winnow to suppress duplicated, perhaps other consumers as well.

  is the use of the hash enough of a key?  dunno.
 */

#include <openssl/sha.h>
#include <time.h>
#include "uthash.h"

/*
  get time string conversion routines.
 */
#include "sr_config.h"

#include "sr_cache.h"


int sr_cache_check( struct sr_cache_t **cachep, char algo, void *ekey, char *path, char* partstr )
 /* 
   insert new item if it isn't in the cache.
   retun value:
       0 - present, so not added,
       1 - was not present, so added to cache.
      -1 - key too long, could not be inserted anyways, so not present.
 */
{
   struct sr_cache_t *c;
   char e[SR_CACHEKEYSZ];
   struct sr_cache_path_t *p;

   e[0]=algo;
   if (get_sumstrlen(algo) < (SR_CACHEKEYSZ-1)) 
       memset(e+1, 0, SR_CACHEKEYSZ-1);
   memcpy(e+1, ekey, get_sumstrlen(algo) );

   HASH_FIND(hh,(*cachep),e,SR_CACHEKEYSZ,c);

   if (!c) 
   {
       c = (struct sr_cache_t *)malloc(sizeof(struct sr_cache_t));
       memcpy(c->key, e, SR_CACHEKEYSZ );
       c->paths=NULL;
       HASH_ADD_KEYPTR( hh, (*cachep), c->key, SR_CACHEKEYSZ, c );
   }

   for ( p = c->paths; p ; p=p->next )
   { 
          /* compare path and partstr */
           if ( !strcmp(p->path, path) && !strcmp(p->partstr,partstr) ) 
               return(0); /* found in the cache already */
   }

   /* not found, so add path to cache entry */
   p = (struct sr_cache_path_t *)malloc(sizeof(struct sr_cache_path_t));
   clock_gettime( CLOCK_REALTIME, &(p->created) );
   p->path = strdup(path);
   p->partstr = strdup(partstr);
   p->next = c->paths;
   c->paths = p;

   return(1);
}

void sr_cache_clean( struct sr_cache_t **cachep, struct timespec *since )
 /* 
     remove entries in the cache older than since. (resolution is in seconds.)
 */
{
    struct sr_cache_t *c, *tmpc;
   struct sr_cache_path_t *e, *prev, *del;

    HASH_ITER(hh, *cachep, c, tmpc )
    {
        e = c->paths; 
        while ( e )
        {
           if (e->created.tv_sec < since->tv_sec) 
           {
              del=e;

              if (!prev) {
                  c->paths = e->next;
                  prev=e;
              } else {
                  prev->next = e->next; 
              }
              e=e->next;

              free(del->path);
              free(del->partstr);
              free(del);
           } else  {
              e=e->next;
           }
              
        }
        if (! (c->paths) ) {
           HASH_DEL(*cachep,c);
           free(c);
        }
    }
}

void sr_cache_free( struct sr_cache_t **cachep)
 /* 
     remove all entries in the cache  (cleanup to discard.)
 */
{
    struct sr_cache_t *c, *tmpc;
   struct sr_cache_path_t *e, *del ;

    HASH_ITER(hh, (*cachep), c, tmpc )
    {
        HASH_DEL((*cachep),c);
        e = c->paths; 
        while( e )
        {
            del=e;
            e=e->next; 
            free(del->path);
            free(del->partstr);
            free(del);
        }
        free(c);
    }
}

void sr_cache_save( struct sr_cache_t *cache, const char *fn)
 /* 
     remove entries in the cache older than since.

FIXME: doesn't write paths yet...
 */
{
    struct sr_cache_t *c, *tmpc;
    struct sr_cache_path_t *e;
    FILE *f;
    char sumstr[ SR_SUMSTRLEN ];

    f = fopen( fn, "w" );
    if ( !f ) 
    {
        fprintf( stderr, "ERROR: failed to open cache file to save: %s\n", fn );
        return;
    }
    HASH_ITER(hh, cache, c, tmpc )
    {
       sumstr[0]=c->key[0];
       sumstr[1]=',';
       for (int i=1; i <= get_sumstrlen(c->key[0]); i++ )
           sprintf( &(sumstr[i*2]), "%02x", (unsigned char)(c->key[i]));
       for ( e = c->paths; e ; e=e->next )
       {       
          fprintf(f,"%s %s %s %s\n", sumstr, sr_time2str( &(e->created) ), e->path, e->partstr );
       }
    }
    fclose(f);
}

int convert_hex_digit( char c )
 /* return ordinal value of digit assuming a character set that has a-f sequential in both lower and upper case.
    kind of based on ASCII, because numbers are assumed to be lower in collation than upper and lower case letters.
FIXME: doesn't read paths yet...
  */
{
   if ( c < ':' ) return(c - '0');
   if ( c < 'F' ) return(c - 'A' + 10);
   if ( c < 'f' ) return(c - 'a' + 10);
   return(-1);
}


#define load_buflen (SR_CACHEKEYSZ*2 + SR_TIMESTRLEN + PATH_MAX + 24)

static char buf[ load_buflen ];

struct sr_cache_t *sr_cache_load( const char *fn)
 /* 
     create an sr_cache based on the content of the named file.     
 */
{
    struct sr_cache_t *c, *cache;
    struct sr_cache_path_t *p;
    char *sum, *timestr, *path, *partstr;
    char key_val[SR_CACHEKEYSZ]; 
    FILE *f;
    int line_count=0;

    f = fopen( fn, "r" );
    if ( !f ) 
    {
        fprintf( stderr, "ERROR: failed to open cache file to load: %s\n", fn );
        return(NULL);
    }
    cache = NULL;

    while( fgets( buf, load_buflen, f ) )
    {
       line_count++;
       fprintf( stderr, "strlen(buf)=%ld loadbuflen: %d\n", strlen(buf), load_buflen );
       sum = strtok( buf, " " );
   
       if (!sum) 
       {
           fprintf( stderr, "corrupt line in cache file %s: %s\n", fn, buf );
           continue;
       }

       timestr = strtok( NULL, " " );
   
       if (!timestr) 
       {
           fprintf( stderr, "no timestring, corrupt line in cache file %s: %s\n", fn, buf );
           continue;
       }

       path = strtok( NULL, " " );
   
       if (!path) 
       {
           fprintf( stderr, "no path, corrupt line in cache file %s: %s\n", fn, buf );
           continue;
       }

       partstr = strtok( NULL, " \n" );
   
       if (!partstr) 
       {
           fprintf( stderr, "no partstr, corrupt line in cache file %s: %s\n", fn, buf );
           continue;
       }

       fprintf( stderr, "fields: sum=+%s+, timestr=+%s+, path=+%s+, partstr=+%s+\n", 
           sum, timestr, path, partstr );

       memset( key_val, 0, SR_CACHEKEYSZ );
       key_val[0] = buf[0];
       for (int i=1; i <= get_sumstrlen(buf[0]) ; i++ ) 
       {
            key_val[i]= convert_hex_digit(sum[2*i]) * 16 + convert_hex_digit(sum[2*i+1])  ;
       }

       HASH_FIND(hh,cache, key_val,SR_CACHEKEYSZ,c);

       if (!c) {
           c = (struct sr_cache_t *)malloc(sizeof(struct sr_cache_t));
           if (!c) 
           {
               fprintf( stderr, "out of memory reading cache file: %s, stopping at line: %s\n", fn, buf  );
               return(cache);
           }

           memcpy(c->key, key_val, SR_CACHEKEYSZ );
           c->paths=NULL;
           HASH_ADD_KEYPTR( hh, cache, c->key, SR_CACHEKEYSZ, c );
       }
       /* assert, c != NULL */

       /* add path to cache entry */
       p = (struct sr_cache_path_t *)malloc(sizeof(struct sr_cache_path_t));
       if (!c) 
       {
           fprintf( stderr, "out of memory 2, reading cache file: %s, stopping at line: %s\n", fn, buf  );
           return(cache);
       }

       memcpy( &(p->created), sr_str2time( timestr ), sizeof(struct timespec) );
       p->path = strdup(path);
       p->partstr = strdup(partstr);
       p->next = c->paths;
       c->paths = p;

    }
    fclose(f);
    return(cache);
}


#ifdef __cplusplus
#include <cstdint>
extern "C"{
#else
#include <stdint.h>
#endif

  void histogram_epanechnikov(uint8_t *vs, double *freq, double *offset, double *size, int32_t *embed);
  void histogram_gauss(uint8_t *vs, double *freq, double *offset, double *size, int32_t *embed);

  void meanshift_epanechnikov(uint8_t *vs, double *weight, double *offset, double *size, int32_t *embed);
  void meanshift_gauss(uint8_t *vs, double *weight, double *offset, double *size, int32_t *embed);

#ifdef __cplusplus
}
#endif


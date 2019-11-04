
#ifdef __cplusplus
extern "C"{
#endif

  void histogram_epanechnikov(uint8_t *vs, double *freq, double *offset, double *size, int *embed);
  void histogram_gauss(uint8_t *vs, double *freq, double *offset, double *size, int *embed);

  void meanshift_epanechnikov(uint8_t *vs, double *weight, double *offset, double *size, int *embed);
  void meanshift_gauss(uint8_t *vs, double *weight, double *offset, double *size, int *embed);

#ifdef __cplusplus
}
#endif

